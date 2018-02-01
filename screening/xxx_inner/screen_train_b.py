import pandas as pd
import numpy as np
import os
import shutil

root = '/media/weidong/weidong/12.15质检图片'
root_b = os.path.join(root, 'train_b')
all_b = os.path.join(root, 'all1')
os.makedirs(root_b, exist_ok=True)

for i in range(3):
    tmp_root = os.path.join(root_b, str(i))
    os.makedirs(tmp_root, exist_ok=True)

df_0 = pd.DataFrame.from_csv('b0_data_multi.csv')
df_1 = pd.DataFrame.from_csv('b1_data_multi.csv')
df_2 = pd.DataFrame.from_csv('b2_data_multi.csv')

df_list = []
df_list.append(df_0)
df_list.append(df_1)
df_list.append(df_2)

for i, df in enumerate(df_list):
    for index, row in df.iterrows():
        dst_file = os.path.join(root_b, '{}/{}.jpg'.format(i, row['image']))
        src_file = os.path.join(all_b, '{}.jpg'.format(row['image']))
        shutil.copy(src_file, dst_file)
        print('====> copy from {} to {}'.format(src_file, dst_file))


