import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split

a_raw_csv = '../xxx/a_data_multi.csv'
b_raw_csv = '../xxx/b_data_multi.csv'

df_a = pd.DataFrame.from_csv(a_raw_csv)
df_b = pd.DataFrame.from_csv(b_raw_csv)

assert df_a.index.size == df_b.index.size

randindex = np.random.permutation(df_a.index.size)

cnt = int(df_a.index.size/3)

df_a0 = df_a[:cnt]
df_a1 = df_a[cnt:cnt*2]
df_a2 = df_a[cnt*2:]

df_b0 = df_b[:cnt]
df_b1 = df_b[cnt:cnt*2]
df_b2 = df_b[cnt*2:]

df_a0.to_csv('a0_data_multi.csv')
df_a1.to_csv('a1_data_multi.csv')
df_a2.to_csv('a2_data_multi.csv')

df_b0.to_csv('b0_data_multi.csv')
df_b1.to_csv('b1_data_multi.csv')
df_b2.to_csv('b2_data_multi.csv')

df_a01b01 = pd.concat([df_a0, df_a1, df_b0, df_b1])
df_a02b02 = pd.concat([df_a0, df_a2, df_b0, df_b2])
df_a12b12 = pd.concat([df_a1, df_a2, df_b1, df_b2])

test_ratio = 0.2
val_ratio = 0.1

test_cnt = int(df_a01b01.index.size * 0.2)
val_cnt = int(df_a01b01.index.size * 0.1)
df_a01b01_train = df_a01b01[:-(test_cnt+val_cnt)]
df_a01b01_val = df_a01b01[-(test_cnt+val_cnt):-test_cnt]
df_a01b01_test = df_a01b01[-test_cnt:]
df_a01b01.to_csv('mix01_data_multi.csv')
df_a01b01_train.to_csv('mix01_train_multi.csv')
df_a01b01_val.to_csv('mix01_val_multi.csv')
df_a01b01_test.to_csv('mix01_test_multi.csv')

test_cnt = int(df_a02b02.index.size * 0.2)
val_cnt = int(df_a02b02.index.size * 0.1)
df_a02b02_train = df_a02b02[:-(test_cnt+val_cnt)]
df_a02b02_val = df_a02b02[-(test_cnt+val_cnt):-test_cnt]
df_a02b02_test = df_a02b02[-test_cnt:]
df_a02b02.to_csv('mix02_data_multi.csv')
df_a02b02_train.to_csv('mix02_train_multi.csv')
df_a02b02_val.to_csv('mix02_val_multi.csv')
df_a02b02_test.to_csv('mix02_test_multi.csv')

test_cnt = int(df_a12b12.index.size * 0.2)
val_cnt = int(df_a12b12.index.size * 0.1)
df_a12b12_train = df_a12b12[:-(test_cnt+val_cnt)]
df_a12b12_val = df_a12b12[-(test_cnt+val_cnt):-test_cnt]
df_a12b12_test = df_a12b12[-test_cnt:]
df_a12b12.to_csv('mix12_data_multi.csv')
df_a12b12_train.to_csv('mix12_train_multi.csv')
df_a12b12_val.to_csv('mix12_val_multi.csv')
df_a12b12_test.to_csv('mix12_test_multi.csv')