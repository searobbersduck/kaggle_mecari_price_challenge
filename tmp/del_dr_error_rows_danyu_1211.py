'''

1. delete data where "ground truth == 0" but "predict == 3 or 4"
2. delete data where "ground truth == 1" but "predict == 3 or 4"
3. delete data where "ground truth == 2" but "predict == 3 or 4"

'''

csv_data = 'data_multi.csv'
csv_train = 'train_multi.csv'
csv_val = 'val_multi.csv'
csv_test = 'test_multi.csv'

csv_result0 = '0_result.csv'
csv_result1 = '1_result.csv'
csv_result2 = '2_result.csv'
csv_result3 = '3_result.csv'
csv_result4 = '4_result.csv'

import pandas as pd

df_data = pd.DataFrame.from_csv(csv_data)
print('origin data shape:')
print(df_data.shape)
df_res0 = pd.DataFrame.from_csv(csv_result0)
df_res2 = pd.DataFrame.from_csv(csv_result2)
df_res1 = pd.DataFrame.from_csv(csv_result1)
df_res3 = pd.DataFrame.from_csv(csv_result3)
df_res4 = pd.DataFrame.from_csv(csv_result4)
df_res0_del = df_res0[(df_res0['dr_level'] != 0)]
df_res1_del = df_res1[(df_res1['dr_level'] != 1)]
df_res2_del = df_res2[(df_res2['dr_level'] != 2)]
df_res3_del = df_res3[(df_res3['dr_level'] != 3)]
df_res4_del = df_res4[(df_res4['dr_level'] != 4)]
print('======> need to delete where "ground truth == 0" but "predict result == 3 or 4": ')
print(df_res0_del.shape)
print('======> need to delete where "ground truth == 1" but "predict result == 3 or 4": ')
print(df_res1_del.shape)
print('======> need to delete where "ground truth == 2" but "predict result == 3 or 4": ')
print(df_res2_del.shape)

print('\n')
print('delete where "ground truth == 0" but "predict result == 3 or 4": ')
for item in df_res0_del['image']:
    df_data.drop(df_data.loc[df_data['image'] == item.split('.')[0]].index[0], inplace=True)

print('\n')
print('delete where "ground truth == 1" but "predict result == 3 or 4": ')
for item in df_res1_del['image']:
    try:
        df_data.drop(df_data.loc[df_data['image'] == item.split('.')[0]].index[0], inplace=True)
    except:
        continue

print('\n')
print('delete where "ground truth == 2" but "predict result == 3 or 4": ')
for item in df_res2_del['image']:
    df_data.drop(df_data.loc[df_data['image'] == item.split('.')[0]].index[0], inplace=True)

print('====> dataset size after delete where "ground truth == 0 or 1 or 2" but "predict result == 3 or 4": ')
print(df_data.shape)

'''
split data into 3 dataset: train, validation, test
'''

for item in df_res3_del['image']:
    df_data.drop(df_data.loc[df_data['image'] == item.split('.')[0]].index[0], inplace=True)
for item in df_res4_del['image']:
    df_data.drop(df_data.loc[df_data['image'] == item.split('.')[0]].index[0], inplace=True)




testratio = 0.2
valratio = 0.1

from sklearn.cross_validation import train_test_split

df_train, df_test = train_test_split(df_data, test_size=testratio)
df_train, df_val = train_test_split(df_train, test_size=valratio)

import os
sub_dir = 'del34_danyu_1211'
os.makedirs(sub_dir, exist_ok=True)
out_csv_data = os.path.join(sub_dir, csv_data)
out_csv_train = os.path.join(sub_dir, csv_train)
out_csv_val = os.path.join(sub_dir, csv_val)
out_csv_test = os.path.join(sub_dir, csv_test)

df_data.to_csv(out_csv_data)
df_train.to_csv(out_csv_train)
df_val.to_csv(out_csv_val)
df_test.to_csv(out_csv_test)