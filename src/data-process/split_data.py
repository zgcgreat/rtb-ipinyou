# _*_ coding: utf-8 _*_

from csv import DictReader,reader
from datetime import datetime

origing_data = '../data/train.log.txt'
train_data = '../data/'
test_data = '../data/'


def split_data(date):
    with open(train_data+'train{}.csv'.format(date), 'w') as f1, open(test_data+'test{}.csv'.format(date), 'w') as f2:
        fi = open(origing_data, 'r')
        header = next(fi).replace('\t', ',')
        f1.write(header.replace('\t', ','))
        f2.write(header.replace('\t', ','))
        for line in fi:
            s = line.strip().split('\t')
            day = s[4][6:8]
            usertag = s[-1]
            if usertag == '\n' or len(usertag) == 0:
                usertag = 'null'
            else:
                usertag = usertag.strip().replace(',', '')
            if int(day) < date:
                for i in range(len(s) - 1):
                    f1.write(s[i] + ',')
                f1.write(usertag + '\n')
            if int(day) == date:
                for i in range(len(s) - 1):
                    f2.write(s[i] + ',')
                f2.write(usertag + '\n')
    f1.close()
    f2.close()
    fi.close()


if __name__ == '__main__':
    split_data(11)
    split_data(12)
    print('train and test data are prepared !')