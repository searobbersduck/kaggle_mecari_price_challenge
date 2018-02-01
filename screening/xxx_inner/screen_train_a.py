import pandas as pd
import numpy as np
import os
import shutil

root_dst = '/media/weidong/weidong/12.15质检图片'
root_src_1 = '/home/weidong/data/LabelImages'
root_src_0 = '/home/weidong/data/NormalData'
root_a = os.path.join(root_dst, 'train_a')

os.makedirs(root_a, exist_ok=True)

for i in range(3):
    tmp_root = os.path.join(root_a, str(i))
    os.makedirs(tmp_root, exist_ok=True)

df_0 = pd.DataFrame.from_csv('a0_data_multi.csv')
df_1 = pd.DataFrame.from_csv('a1_data_multi.csv')
df_2 = pd.DataFrame.from_csv('a2_data_multi.csv')

df_list = []
df_list.append(df_0)
df_list.append(df_1)
df_list.append(df_2)

for i, df in enumerate(df_list):
    for index, row in df.iterrows():
        dst_file = os.path.join(root_a, '{}/{}.jpg'.format(i, row['image']))
        if row['dr_level'] == 0:
            src_file = os.path.join(root_src_0, '{}.jpg'.format(row['image']))
        else:
            src_file = os.path.join(os.path.join(root_src_1, '{}'.format(row['dr_level'])), '{}.jpg'.format(row['image']))
        shutil.copy(src_file, dst_file)
        print('====> copy from {} to {}'.format(src_file, dst_file))


