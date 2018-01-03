import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = 'hpg_reserve.csv'

df = pd.DataFrame.from_csv(csv_file)

print(df.shape)
print(df.columns.values)
print(df.head(n=5))

grouped_by_id = df.groupby('hpg_store_id')
print('id count: ')
print(len(grouped_by_id.groups))

df['reserve_datetime'] = df['reserve_datetime'].apply(
    lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()
).astype('datetime64[ns]')

df['visit_datetime'] = df['visit_datetime'].apply(
    lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()
).astype('datetime64[ns]')

grouped_by_reserve_datetime = df.groupby(['reserve_datetime'])
grouped_by_reserve_datetime['reserve_visitors'].sum().plot(legend=True, figsize=(20,5))
plt.show()