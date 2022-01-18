import torch
# import torch.nn as nn
# import argparse
# from sklearn.metrics import jaccard_score, roc_auc_score, precision_score, f1_score, average_precision_score
# import numpy as np
import dill
# import time
# from torch.nn import CrossEntropyLoss
# from torch.optim import Adam
# import os
# import torch.nn.functional as F
# import random
# from collections import defaultdict
#
# import sys
# sys.path.append("..")
# from models import Leap
# from util import llprint, sequence_metric, sequence_output_process, ddi_rate_score, get_n_params
#
# torch.manual_seed(1203)
#
# # os.environ["CUDA_VISIBLE_DEVICES"] = "3"
#
# model_name = 'Leap'
# resume_path = 'saved/{}/Epoch_49_JA_0.4603_DDI_0.07427.model'.format(model_name)
#
# if not os.path.exists(os.path.join("saved", model_name)):
#         os.makedirs(os.path.join("saved", model_name))
#
# # Training settings
# parser = argparse.ArgumentParser()
# parser.add_argument('--Test', action='store_true', default=False, help="test mode")
# parser.add_argument('--model_name', type=str, default=model_name, help="model name")
# parser.add_argument('--resume_path', type=str, default=resume_path, help='resume path')
# parser.add_argument('--lr', type=float, default=0.0005, help='learning rate')
#
# args = parser.parse_args()
#
#
#
#
# # load data
# data_path = '../data/records_final.pkl'
# voc_path = '../data/voc_final.pkl'
# device = torch.device('cuda')
#
# data = dill.load(open(data_path, 'rb'))
# voc = dill.load(open(voc_path, 'rb'))
# diag_voc, pro_voc, med_voc = voc['diag_voc'], voc['pro_voc'], voc['med_voc']
#
# split_point = int(len(data) * 2 / 3)
# data_train = data[:split_point]
# eval_len = int(len(data[split_point:]) / 2)
# data_test = data[split_point:split_point + eval_len]
# data_eval = data[split_point+eval_len:]
# voc_size = (len(diag_voc.idx2word), len(pro_voc.idx2word), len(med_voc.idx2word))
# admission_count = 0
# for patient in data:
#         admission_count += len(patient)
# print(admission_count)
# # for patient in data:
# #         print(patient)
#
#
# END_TOKEN = voc_size[2] + 1
#
# model = Leap(voc_size, device=device)
# model.to(device=device)
# print('parameters', get_n_params(model))
# optimizer = Adam(model.parameters(), lr=args.lr)
# history = defaultdict(list)
# best_epoch, best_ja = 0, 0
# EPOCH = 50
# for epoch in range(EPOCH):
#         tic = time.time()
#         print('\nepoch {} --------------------------'.format(epoch + 1))
#
#         model.train()
#         for step, input in enumerate(data_train):
#                 for adm in input:
#                         loss_target = adm[2] + [END_TOKEN]
#                         output_logits = model(adm)
#                         loss = F.cross_entropy(output_logits, torch.LongTensor(loss_target).to(device))
#                         optimizer.zero_grad()
#                         loss.backward(retain_graph=True)
#                         optimizer.step()
#
#                 llprint('\rtraining step: {} / {}'.format(step, len(data_train)))
#
#         print()
#         tic2 = time.time()
#         ddi_rate, ja, prauc, avg_p, avg_r, avg_f1, avg_med = eval(model, data_eval, voc_size, epoch)
#         print('training time: {}, test time: {}'.format(time.time() - tic, time.time() - tic2))
#
#         history['ja'].append(ja)
#         history['ddi_rate'].append(ddi_rate)
#         history['avg_p'].append(avg_p)
#         history['avg_r'].append(avg_r)
#         history['avg_f1'].append(avg_f1)
#         history['prauc'].append(prauc)
#         history['med'].append(avg_med)
#
#         if epoch >= 5:
#                 print('ddi: {}, Med: {}, Ja: {}, F1: {}, PRAUC: {}'.format(
#                         np.mean(history['ddi_rate'][-5:]),
#                         np.mean(history['med'][-5:]),
#                         np.mean(history['ja'][-5:]),
#                         np.mean(history['avg_f1'][-5:]),
#                         np.mean(history['prauc'][-5:])
#                 ))
#

# import torch
#
# list1 = [2.5] * 72
# print(list1)
# print(torch.tensor(list1).unsqueeze(dim=0))


# data_path = '../data/records_final_72features.pkl'
# voc_path = '../data/voc_final_72features.pkl'
# device = torch.device('cuda')
# voc = dill.load(open(voc_path, 'rb'))
# diag_voc, pro_voc, med_voc = voc['diag_voc'], voc['pro_voc'], voc['med_voc']
# print(med_voc.word2idx)

# data = dill.load(open(data_path, 'rb'))
# for patient in data:
#         # print(patient)
#         for admission in patient:
#                 print(admission[2])

history_path = "/code/pinkpig/KDD_TX/SafeDrug/SafeDrug-main/src/saved/Leap1/history_Leap1.pkl"
device = torch.device('cuda')
history = dill.load(open(history_path, 'rb'))
print(history)