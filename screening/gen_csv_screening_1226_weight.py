import os
import pandas as pd
from glob import glob
import numpy as np
from sklearn.cross_validation import train_test_split
import random

'''

add weight for "ground truth==4" but "predict==0"

'''


# root_0 = '/home/weidong/data/sort_image/pure'
root_0 = '/home/weidong/data/sort_image1/8k0'
dir_0_list = [
    'sort2_finish/0_finished', 'sort15_finish/0', 'sort16_finish/0', 'sort17_finish/0', 'sort19_finish', 'sort18_finish/0',
]
root_other = '/home/weidong/data/LabelImages'

list_0 = []
for dir in dir_0_list:
    rule = os.path.join(root_0, '{}/*.jpg'.format(dir))
    tmp_list = glob(rule)
    list_0 += tmp_list
root_0_add = '/media/weidong/weidong/0补充-暗'
tmp_list = glob(os.path.join(root_0_add, '*.jpg'))
list_0 += tmp_list


list_1 = glob(os.path.join(root_other, '1/*.jpg'))
list_2 = glob(os.path.join(root_other, '2/*.jpg'))
list_3 = glob(os.path.join(root_other, '3/*.jpg'))
list_4 = glob(os.path.join(root_other, '4/*.jpg'))

csv_list = glob(os.path.join(root_other, '4/*.csv'))
# csv_4 = os.path.join(root_other, '4/result.csv')
list_error_4 = []
for csv_file in csv_list:
    df_4 = pd.DataFrame.from_csv(csv_file)
    for index, row in df_4.iterrows():
        if row['dr_level'] < 2:
            list_error_4.append(row['image'])

for i in range(50):
    list_4 += list_error_4


randindex = np.random.permutation(len(list_0))
list_0 = [list_0[i] for i in randindex]

randindex = np.random.permutation(len(list_1))
# randindex = randindex[0:20]
list_1 = [list_1[i] for i in randindex]

randindex = np.random.permutation(len(list_2))
# randindex = randindex[0:20]
list_2 = [list_2[i] for i in randindex]

randindex = np.random.permutation(len(list_3))
# randindex = randindex[0:20]
list_3 = [list_3[i] for i in randindex]

randindex = np.random.permutation(len(list_4))
# randindex = randindex[0:20]
list_4 = [list_4[i] for i in randindex]

total_cnt = len(list_0) + len(list_1) + len(list_2) + len(list_3) + len(list_4)
print('{:.1f}'.format(len(list_0)/total_cnt*100))
print('{:.1f}'.format(len(list_1)/total_cnt*100))
print('{:.1f}'.format(len(list_2)/total_cnt*100))
print('{:.1f}'.format(len(list_3)/total_cnt*100))
print('{:.1f}'.format(len(list_4)/total_cnt*100))

print('\n')
print(len(list_0))
print(len(list_1))
print(len(list_2))
print(len(list_3))
print(len(list_4))
print(total_cnt)
print('\n')

dr_level = []
image_list = []

for i in range(len(list_0)):
    dr_level.append(0)
    image_list.append(list_0[i])

for i in range(len(list_1)):
    dr_level.append(1)
    image_list.append(list_1[i])
for i in range(len(list_2)):
    dr_level.append(2)
    image_list.append(list_2[i])
for i in range(len(list_3)):
    dr_level.append(3)
    image_list.append(list_3[i])
for i in range(len(list_4)):
    dr_level.append(4)
    image_list.append(list_4[i])

image_list = [os.path.basename(i).split('.')[0] for i in image_list]

dme_level = []
referable_level = []

for i, dr in enumerate(dr_level):
    dme = dr if dr < 4 else 3
    dme_level.append(dme)
    ref = 0 if dr < 2 else 1
    referable_level.append(ref)

assert len(image_list) == len(dr_level) == len(dme_level) == len(referable_level)


# random
randindex = np.random.permutation(len(image_list))
image_list = [image_list[i] for i in randindex]
dr_level = [dr_level[i] for i in randindex]
dme_level = [dme_level[i] for i in randindex]
referable_level = [referable_level[i] for i in randindex]



test_ratio = 0.2
val_ratio = 0.1

data = np.column_stack((image_list, dr_level, dme_level, referable_level))

train_data, test_data = train_test_split(data, test_size=test_ratio)
train_data, val_data = train_test_split(train_data, test_size=val_ratio)

data_df = pd.DataFrame(data, columns=['image', 'dr_level', 'dme_level', 'referable'])
train_df = pd.DataFrame(train_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
val_df = pd.DataFrame(val_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
test_df = pd.DataFrame(test_data, columns=['image', 'dr_level', 'dme_level', 'referable'])

csv_root = './screen_flag_1226_add_weight'
os.makedirs(csv_root, exist_ok=True)

csv_data = os.path.join(csv_root, 'data_multi.csv')
csv_train = os.path.join(csv_root, 'train_multi.csv')
csv_val = os.path.join(csv_root, 'val_multi.csv')
csv_test = os.path.join(csv_root, 'test_multi.csv')

data_df.to_csv(csv_data)
train_df.to_csv(csv_train)
val_df.to_csv(csv_val)
test_df.to_csv(csv_test)
