import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = 'hpg_store_info.csv'

df = pd.DataFrame.from_csv(csv_file)

print(df.shape)
print(df.columns.values)
print(df.head(n=5))


# plt.figure(figsize=(15,15))
# plt.scatter(df['longitude'], df['latitude'], s=20)
#
# plt.show()


# combine 'hpg_store_info' and 'hpg_reserve'
df_reserve = pd.DataFrame.from_csv('hpg_reserve.csv')
print('====> reserve info: ')
print(df_reserve.shape)
print(df_reserve.columns.values)
print(df_reserve.head(n=5))

df_merge = pd.merge(df_reserve, df, left_index=True, right_index=True, how='inner')
print('====> merge info: ')
print(df_merge.shape)
print(df_merge.columns.values)
print(df_merge.head(n=5))

grouped_by_id = df_merge.groupby(['hpg_store_id'])
print(grouped_by_id['reserve_visitors'].sum().shape)

grouped_by_id['reserve_visitors'].sum().plot()
plt.show()

print('hello world')
