import os
import pandas as pd


train_file = '/home/weidong/data/kaggle/Mercari/train.tsv'

cnt = 0

train_data = []

with open(train_file, 'r') as f:
    for line in f:
        cnt += 1
        if cnt == 1000:
            break;
        train_data.append(line.strip().split('\t'))
        print(line)

columns = train_data[0]
train_data = train_data[1:]

train_df = pd.DataFrame(train_data, columns=columns)

csv_train = './train.csv'

train_df.to_csv(csv_train)