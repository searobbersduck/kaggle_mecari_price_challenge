csv_pred = './jianbin.csv'
csv_gt = './doc.csv'

import pandas as pd

df_pred = pd.DataFrame.from_csv(csv_pred)
df_gt = pd.DataFrame.from_csv(csv_gt)

print('pred shape: ')
print(df_pred.shape)
print('gt shape: ')
print(df_gt.shape)

# 1. delete zero
df_gt_reserve = df_gt[(df_gt['dr_level'] > 0.5)|(df_gt['dr_level'].isnull())]
print('gt reserve: ')
print(df_gt_reserve.shape)

# 2. delete
df_copy = df_pred.copy()
for index, row in df_pred.iterrows():
    if int(row['image'].split('.')[0]) in df_gt_reserve.index.tolist():
        df_copy.loc[index,'dme_level'] = df_gt_reserve.iloc[
            df_gt_reserve.index.tolist().index(int(row['image'].split('.')[0]))
        ]['dr_level']
        print(df_gt_reserve.iloc[
            df_gt_reserve.index.tolist().index(int(row['image'].split('.')[0]))
        ]['dr_level'])
        # df_copy.loc.__setitem__((slice(index), ('dme_level')), 5)
        continue
    if row['dr_level'] != 0:
        # df_copy.loc.__setitem__((slice(index), ('dme_level')), 0)
        df_copy.loc[index, 'dme_level'] = 0
        continue
    df_copy.drop(index, axis=0, inplace=True)

print('df_copy: ')
print(df_copy.shape)

df_copy.to_csv('./zhengli.csv')


