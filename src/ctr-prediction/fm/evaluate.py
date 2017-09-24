# _*_ coding: utf-8 _*_


import sys
from csv import DictReader

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score

path = '../output/fm/'

threshold = 0.5

label_path = path + 'validation.csv'
predict_path = path + 'submission.csv'

label_reader = DictReader(open(label_path))
predict_reader = DictReader(open(predict_path))

count = 0
y_true = []
y_pred = []
y_scores = []
for t, row in enumerate(label_reader):
    predict = predict_reader.__next__()
    actual = float(row['label'])
    predicted = float(predict['prob'])
    y_true.append(actual)
    y_scores.append(predicted)

    # 大于阈值的即视为点击
    if predicted >= threshold:
        y_pred.append(1)
    else:
        y_pred.append(0)
    count += 1

# 计算性能指标
auc = roc_auc_score(y_true, y_scores)
logloss = log_loss(y_true, y_scores)
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print('Accuracy: {0}    Precision: {1}    Recall: {2}    F1-Measure: {3}\n'.format(accuracy, precision, recall, f1))
print('logloss: {0}  auc: {1}\n'.format(logloss, auc))

# 将结果写入表格
# statistics = open(path + 'result.csv', 'w')
# statistics.writelines('Accuracy,Precision,Recall,F1-Measure,Logloss,AUC\n')
# statistics.writelines('{0},{1},{2},{3},{4},{5}'.format(accuracy, precision, recall, f1, logloss, auc))
# statistics.close()
# 
# file = open(path + 'validation.csv', 'r')
# next(file)
# clks = 0
# ids = []
# for line in file:
#     id = line.split(',')[0]
#     clk = line.split(',')[1]
#     if int(clk) == 1:
#         clks += 1
#         ids.append(id)
# file.close()
# print('总点击数:', clks)
# 
# 
# f2 = open(path + 'submission.csv', 'r')
# next(f2)
# pred = 0
# true = 0
# for line in f2:
#     id = line.split(',')[0]
#     ctr = line.split(',')[1]
#     if float(ctr) >= threshold:
#         pred += 1
#         if id in ids:
#             true += 1
# 
# f2.close()
# print('预测为1的个数:', pred)
# print('真实为1的个数:', true)

