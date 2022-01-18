import os
os.environ["CUDA_VISIBLE_DIVICES"]="3"
import torch

import torch.nn as nn
import argparse
from sklearn.metrics import jaccard_score, roc_auc_score, precision_score, f1_score, average_precision_score
import numpy as np
import dill
import time
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
import os
import torch.nn.functional as F
import random
from collections import defaultdict

import sys

sys.path.append("..")
from models import Leap1
from util import llprint, sequence_metric, sequence_output_process, ddi_rate_score, get_n_params

torch.manual_seed(1203)

# os.environ["CUDA_VISIBLE_DEVICES"] = "3"

model_name = 'Leap1_ndc'
resume_path = 'saved/{}/Epoch_19_JA_0.4478_DDI_0.07848.model'.format(model_name)

if not os.path.exists(os.path.join("saved", model_name)):
    os.makedirs(os.path.join("saved", model_name))

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('--Test', action='store_true', default=False, help="test mode")
parser.add_argument('--model_name', type=str, default=model_name, help="model name")
parser.add_argument('--resume_path', type=str, default=resume_path, help='resume path')
parser.add_argument('--lr', type=float, default=0.0005, help='learning rate')

args = parser.parse_args()


# evaluate
def eval(model, data_eval, voc_size, epoch):
    model.eval()

    ja, prauc, avg_p, avg_r, avg_f1 = [[] for _ in range(5)]
    smm_record = []
    med_cnt, visit_cnt = 0, 0

    for step, input in enumerate(data_eval):
        y_gt = []
        y_pred = []
        y_pred_prob = []
        y_pred_label = []

        for adm_index, adm in enumerate(input):
            output_logits = model(adm)

            y_gt_tmp = np.zeros(voc_size[2])
            y_gt_tmp[adm[2]] = 1
            y_gt.append(y_gt_tmp)

            # prediction prod
            output_logits = output_logits.detach().cpu().numpy()

            # prediction med set
            out_list, sorted_predict = sequence_output_process(output_logits, [voc_size[2], voc_size[2] + 1])
            y_pred_label.append(sorted(sorted_predict))
            y_pred_prob.append(np.mean(output_logits[:, :-2], axis=0))

            # prediction label
            y_pred_tmp = np.zeros(voc_size[2])
            y_pred_tmp[out_list] = 1
            y_pred.append(y_pred_tmp)
            visit_cnt += 1
            med_cnt += len(sorted_predict)

        smm_record.append(y_pred_label)

        adm_ja, adm_prauc, adm_avg_p, adm_avg_r, adm_avg_f1 = \
            sequence_metric(np.array(y_gt), np.array(y_pred), np.array(y_pred_prob), np.array(y_pred_label))
        ja.append(adm_ja)
        prauc.append(adm_prauc)
        avg_p.append(adm_avg_p)
        avg_r.append(adm_avg_r)
        avg_f1.append(adm_avg_f1)
        llprint('\rtest step: {} / {}'.format(step, len(data_eval)))

    # ddi rate
    # ddi_rate = ddi_rate_score(smm_record, path='../data/ddi_A_final.pkl')

    llprint(
        '\n Jaccard: {:.4},  PRAUC: {:.4}, AVG_PRC: {:.4}, AVG_RECALL: {:.4}, AVG_F1: {:.4}, AVG_MED: {:.4}\n'.format(
             np.mean(ja), np.mean(prauc), np.mean(avg_p), np.mean(avg_r), np.mean(avg_f1), med_cnt / visit_cnt
        ))

    return  np.mean(ja), np.mean(prauc), np.mean(avg_p), np.mean(avg_r), np.mean(avg_f1), med_cnt / visit_cnt


def main():
    # load data
    data_path = '../data/records_final_72features_ndc.pkl'
    voc_path = '../data/voc_final_72features_ndc.pkl'
    device = torch.device('cuda')
    data = dill.load(open(data_path, 'rb'))
    voc = dill.load(open(voc_path, 'rb'))
    diag_voc, pro_voc, med_voc = voc['diag_voc'], voc['pro_voc'], voc['med_voc']

    split_point = int(len(data) * 2 / 3)
    data_train = data[:split_point]
    eval_len = int(len(data[split_point:]) / 2)
    data_test = data[split_point:split_point + eval_len]
    data_eval = data[split_point + eval_len:]
    voc_size = (len(diag_voc.idx2word), len(pro_voc.idx2word), len(med_voc.idx2word), 72)

    END_TOKEN = voc_size[2] + 1

    model = Leap1(voc_size, device=device)
    # model.load_state_dict(torch.load(open(args.resume_path, 'rb')))

    if args.Test:
        model.load_state_dict(torch.load(open(args.resume_path, 'rb')))
        model.to(device=device)
        tic = time.time()
        result = []
        for _ in range(10):
            test_sample = np.random.choice(data_test, round(len(data_test) * 0.8), replace=True)
            ja, prauc, avg_p, avg_r, avg_f1, avg_med = eval(model, test_sample, voc_size, 0)
            result.append([ja, avg_f1, prauc, avg_med])

        result = np.array(result)
        mean = result.mean(axis=0)
        std = result.std(axis=0)

        outstring = ""
        for m, s in zip(mean, std):
            outstring += "{:.4f} $\pm$ {:.4f} & ".format(m, s)

        print(outstring)
        print('test time: {}'.format(time.time() - tic))
        return

    model.to(device=device)
    print('parameters', get_n_params(model))
    optimizer = Adam(model.parameters(), lr=args.lr)

    history = defaultdict(list)
    best_epoch, best_ja = 0, 0

    EPOCH = 50
    for epoch in range(EPOCH):
        tic = time.time()
        print('\nepoch {} --------------------------'.format(epoch + 1))

        model.train()
        for step, input in enumerate(data_train):
            for adm in input:
                loss_target = adm[2] + [END_TOKEN]
                output_logits = model(adm)
                loss = F.cross_entropy(output_logits, torch.LongTensor(loss_target).to(device))
                optimizer.zero_grad()
                loss.backward(retain_graph=True)
                optimizer.step()

            llprint('\rtraining step: {} / {}'.format(step, len(data_train)))

        print()
        tic2 = time.time()
        ja, prauc, avg_p, avg_r, avg_f1, avg_med = eval(model, data_eval, voc_size, epoch)
        print('training time: {}, test time: {}'.format(time.time() - tic, time.time() - tic2))

        history['ja'].append(ja)
        history['avg_p'].append(avg_p)
        history['avg_r'].append(avg_r)
        history['avg_f1'].append(avg_f1)
        history['prauc'].append(prauc)
        history['med'].append(avg_med)

        if epoch >= 5:
            print('Med: {}, Ja: {}, F1: {}, PRAUC: {}'.format(
                np.mean(history['med'][-5:]),
                np.mean(history['ja'][-5:]),
                np.mean(history['avg_f1'][-5:]),
                np.mean(history['prauc'][-5:])
            ))

        torch.save(model.state_dict(), open(os.path.join('saved', args.model_name, \
                                                         'Epoch_{}_JA_{:.4}.model'.format(epoch, ja)), 'wb'))

        if epoch != 0 and best_ja < ja:
            best_epoch = epoch
            best_ja = ja

        print('best_epoch: {}'.format(best_epoch))

        dill.dump(history, open(os.path.join('saved', args.model_name, 'history_{}.pkl'.format(args.model_name)), 'wb'))


if __name__ == '__main__':
    main()
    # fine_tune(fine_tune_name='Epoch_1_JA_0.2765_DDI_0.1158.model')
