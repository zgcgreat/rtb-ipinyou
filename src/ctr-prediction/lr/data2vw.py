# _*_ coding: utf-8 _*_
from csv import DictReader

import sys
from datetime import datetime

data_path = '../data/'
save_path = '../output/lr/'

field = ['weekday', 'hour', 'useragent', 'IP', 'region', 'city', 'adexchange', 'domain', 'slotid', 'slotwidth',
         'slotheight', 'slotvisibility', 'slotformat', 'creative', 'keypage', 'advertiser', 'usertag']


with open(save_path + 'train.vw', 'w') as outfile:
    for t, row in enumerate(DictReader(open(data_path + 'train12.csv', 'r')), start=1):
        features = []
        for k, v in row.items():
            if k in field:
                if len(str(v)) > 0:
                    features.append('{0}={1}'.format(k, v))

        if row['click'] == '1':
            label = 1
        else:
            label = -1

        outfile.write('{0} \' |feats {1}\n'.format(label, ' '.join(['{0}'.format(val) for val
                                                                          in features])))
        if t % 100000 == 0:
            print('Line processed: {0}'.format(t))


with open(save_path + 'test.vw', 'w') as outfile, open(save_path + 'validation.csv', 'w') as f_va:
    f_va.write('id,label\n')
    for t, row in enumerate(DictReader(open(data_path + 'test12.csv', 'r')), start=1):
        f_va.write(str(t) + ',' + row['click'] + '\n')
        features = []
        for k, v in row.items():
            if k in field:
                if len(str(v)) > 0:
                    features.append('{0}={1}'.format(k, v))

        if row['click'] == '1':
            label = 1
        else:
            label = -1

        outfile.write('{0} \' |feats {1}\n'.format(label, ' '.join(['{0}'.format(val) for val
                                                                          in features])))
        if t % 100000 == 0:
            print('Line processed: {0}'.format(t))
