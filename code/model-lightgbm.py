import pickle



with open(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\jupyter\model\lightgbm.pkl', 'rb') as f:
    clf_multilabel = pickle.load(f)
print(clf_multilabel.estimators_)

