# _*_ coding: utf-8 _*_
import sys
import collections
from csv import DictReader
from datetime import datetime

date = sys.argv[1]

root_path = '../'

train_path = root_path + 'data/train{}.csv'.format(date)
test_path = root_path + 'data/test{}.csv'.format(date)
train_ffm = root_path + 'output/ffm/train.ffm'
test_ffm = root_path + 'output/ffm/test.ffm'
vali_path = root_path + 'output/ffm/validation.csv'

field = ['weekday', 'hour', 'useragent', 'region', 'city', 'adexchange', 'domain', 'slotid', 'slotwidth',
         'slotheight', 'slotvisibility', 'slotformat', 'creative', 'keypage', 'advertiser', 'usertag']

table = collections.defaultdict(lambda: 0)


# 为特征名建立编号, filed
def field_index(x):
    index = field.index(x)
    return index


def getIndices(key):
    indices = table.get(key)
    if indices is None:
        indices = len(table)
        table[key] = indices
    return indices


feats = set()
with open(train_ffm, 'w') as outfile:
    for e, row in enumerate(DictReader(open(train_path)), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    idx = field_index(k)
                    kv = k + '_' + v
                    features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                    feats.add(kv + '_' + str(getIndices(kv)))

        if e % 100000 == 0:
            print('creating train.ffm...', e)
        outfile.write('{0} {1}\n'.format(row['click'], ' '.join('{0}'.format(val) for val in features)))


with open(test_ffm, 'w') as f1, open(vali_path, 'w') as f2:
    f2.write('id,label'+'\n')
    for t, row in enumerate(DictReader(open(test_path)), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    idx = field_index(k)
                    kv = k + '_' + v
                    # features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                    if kv + '_' + str(getIndices(kv)) in feats:
                        features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                    else:
                        kv = k + '_other'
                        features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                    feats.add(kv + '_' + str(getIndices(kv)))
        if t % 100000 == 0:
            print('creating validation data and test.ffm...', t)
        f1.write('{0} {1}\n'.format(row['click'], ' '.join('{0}'.format(val) for val in features)))
        f2.write(str(t) + ',' + row['click'] + '\n')

f1.close()
f2.close()
