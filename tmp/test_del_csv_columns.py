csv_file = 'data_multi.csv'
res_file = 'result.csv'

import pandas as pd

res_df = pd.DataFrame.from_csv(res_file)
print(res_df.shape)
print(res_df.head(n=4))
res_df_del = res_df[(res_df['dr_level'] == 3)|(res_df['dr_level'] == 4)]
print('======> need to delete where "ground truth == 2" but "predict result == 3 or 4": ')
print(res_df_del.shape)
# print(res_df_del.head(n=4))

csv_df = pd.DataFrame.from_csv(csv_file)
print('====> origin dataset size')
print(csv_df.shape)
# print(csv_df.head(n=4))

for item in res_df_del['image']:
    csv_df.drop(csv_df.loc[csv_df['image'] == item.split('.')[0]].index[0], inplace=True)

print('====> dataset size after delete where "ground truth == 2" but "predict result == 3 or 4": ')
print(csv_df.shape)
