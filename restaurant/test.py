# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from datetime import datetime
#
# csv_file = 'data/air_reserve.csv'
#
# df = pd.read_csv(csv_file, delimiter=',')
#
# print(df.columns.values)
# print(df.head(n=5))
#
# # y = df['reserve_datetime']
# #
# # y = y.apply(lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()).astype('datetime64')
# #
# # y.groupby([ y.dt.year, y.dt.month]).count().plot(kind='bar')
# #
# # plt.show()
#
# zz = df[:500].groupby(['air_store_id', 'reserve_datetime'])
#
# df.set_index('reserve_datetime', inplace=True)
# zz['reserve_visitors'].plot(legend=True)
# plt.show()
#
# zz_21 = df.groupby([
#     'reserve_datetime', 'air_store_id'
# ])
#
# z = df[~df['air_store_id'].duplicated()]
# print(z.shape)
# tmp_id = z['air_store_id'][0]
# id0 = df[df['air_store_id'] == tmp_id]
# print(id0.shape)
# id0['reserve_datetime'] = id0['reserve_datetime'].apply(
#     lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()).astype('datetime64')
# id0_reservedate = id0[['reserve_datetime', 'reserve_visitors']]
# id0_reservedate = id0_reservedate.groupby([id0['reserve_datetime'].dt.year, id0['reserve_datetime'].dt.month]).count()
# print(id0_reservedate.shape)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = 'data/air_reserve.csv'

df = pd.read_csv(csv_file, delimiter=',')

df['reserve_datetime'] = df['reserve_datetime'].apply(lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()).astype('datetime64')
grouped_reserve = df.groupby(['reserve_datetime'])
grouped_reserve['reserve_visitors'].sum().plot(legend=True)
plt.show()
