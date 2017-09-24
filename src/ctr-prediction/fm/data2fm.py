# _*_ coding: utf-8 _*_

import collections
from csv import DictReader
from datetime import datetime

root_path = '../'
train_path = root_path + 'data/train12.csv'
test_path = root_path + 'data/test12.csv'
train_fm = root_path + 'output/fm/train.fm'
test_fm = root_path + 'output/fm/test.fm'
vali_path = root_path + 'output/fm/validation.csv'

field = ['weekday', 'hour', 'useragent', 'IP', 'region', 'city', 'adexchange', 'domain', 'slotid', 'slotwidth',
         'slotheight', 'slotvisibility', 'slotformat', 'creative', 'keypage', 'advertiser', 'usertag']

table = collections.defaultdict(lambda: 0)


def getIndices(key):
    indices = table.get(key)
    if indices is None:
        indices = len(table)
        table[key] = indices
    return indices

feats = set()
with open(train_fm, 'w') as outfile:
    for e, row in enumerate(DictReader(open(train_path)), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    kv = k + '_' + v
                    features.append('{0}:1'.format(getIndices(kv)))
                    feats.add(kv + '_' + str(getIndices(kv)))

        if e % 100000 == 0:
            print('creating train.fm...', e)
        outfile.write('{0} {1}\n'.format(row['click'], ' '.join('{0}'.format(val) for val in features)))

with open(test_fm, 'w') as f1, open(vali_path, 'w') as f2:
    f2.write('id,label'+'\n')
    for t, row in enumerate(DictReader(open(test_path)), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    kv = k + '_' + v
                    if kv + '_' + str(getIndices(kv)) in feats:
                        features.append('{0}:1'.format(getIndices(kv)))
                    else:
                        kv = k + '-other'
                        features.append('{0}:1'.format(getIndices(kv)))
                    feats.add(kv + '_' + str(getIndices(kv)))
        if t % 100000 == 0:
            print('creating validation data and test.fm...', t)
        f1.write('{0} {1}\n'.format(row['click'], ' '.join('{0}'.format(val) for val in features)))
        f2.write(str(t) + ',' + row['click'] + '\n')


