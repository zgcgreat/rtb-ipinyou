# _*_ coding: utf-8 _*_

from csv import DictReader

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# 画roc曲线

root_path = '../output/'
path_ffm = root_path + 'ffm/'
path_fm = root_path + 'fm/'
path_vw = root_path + 'lr/'


def f(path):
    label_path = path + 'validation.csv'
    predict_path = path + 'submission.csv'
    label_reader = DictReader(open(label_path))
    predict_reader = DictReader(open(predict_path))
    y_true = []
    y_scores = []
    for t, row in enumerate(label_reader):
        predict = predict_reader.__next__()
        actual = float(row['label'])
        predicted = float(predict['prob'])
        y_true.append(actual)
        y_scores.append(predicted)
    # Compute ROC curve and ROC area
    fpr, tpr, threshold = roc_curve(y_true, y_scores, pos_label=1)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr, roc_auc

fpr_ffm, tpr_ffm, auc_ffm = f(path_ffm)
fpr_fm, tpr_fm, auc_fm = f(path_fm)
fpr_vw, tpr_vw, auc_vw = f(path_vw)

plt.figure()
lw = 2  # 线宽
plt.plot(fpr_ffm, tpr_ffm, color='blue', lw=lw, label='ROC FFM (area = %0.2f)' % auc_ffm)
plt.plot(fpr_fm, tpr_fm, color='darkorange', lw=lw, label='ROC FM (area = %0.2f)' % auc_fm)
plt.plot(fpr_vw, tpr_vw, color='indigo', lw=lw, label='ROC LR (area = %0.2f)' % auc_vw)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('CTR Prediction')
plt.legend(loc='lower right')
# plt.savefig('roc-auc.png', dpi=100)
plt.show()
