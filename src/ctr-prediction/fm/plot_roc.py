from csv import DictReader

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# 画roc曲线

path = '../../../output/fm/'


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

# Compute ROC curve and ROC area for each class

fpr, tpr, _ = roc_curve(y_true, y_scores, pos_label=1)
roc_auc = auc(fpr, tpr)

plt.figure()
lw = 2  # 线宽
plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC of fm')
plt.legend(loc="lower right")
plt.savefig('{0}/roc_fm.png'.format(path), dpi=100)
plt.show()
