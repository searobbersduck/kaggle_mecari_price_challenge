'''

====> total images number is: 44631. list as follows:
		graded level-0: 29118	65.2%
		graded level-1: 1086	2.4%
		graded level-2: 9773	21.9%
		graded level-3: 1822	4.1%
		graded level-4: 2832	6.3%

'''

import os
import pandas as pd
from glob import glob
import numpy as np
from sklearn.cross_validation import train_test_split
import random
import argparse
import math

def parse_args():
    parser = argparse.ArgumentParser(description='weight')
    parser.add_argument('--ratio2', default=0.5, type=float)
    parser.add_argument('--output', required=True)
    return parser.parse_args()

args = parse_args()


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

cnt_0 = len(list_0)
cnt_1 = int(cnt_0/65.2*2.4)
cnt_2 = int(cnt_0/65.2*21.9)
cnt_3 = int(cnt_0/65.2*4.1)
cnt_4 = int(cnt_0/65.2*6.3)


list_1 = glob(os.path.join(root_other, '1/*.jpg'))
list_2 = glob(os.path.join(root_other, '2/*.jpg'))
list_3 = glob(os.path.join(root_other, '3/*.jpg'))
list_4 = glob(os.path.join(root_other, '4/*.jpg'))

# csv_list = glob(os.path.join(root_other, '4/*.csv'))
# # csv_4 = os.path.join(root_other, '4/result.csv')
# list_error_4 = []
# for csv_file in csv_list:
#     df_4 = pd.DataFrame.from_csv(csv_file)
#     for index, row in df_4.iterrows():
#         if row['dr_level'] < 2:
#             list_error_4.append(row['image'])
#
# for i in range(50):
#     list_4 += list_error_4


randindex = np.random.permutation(len(list_0))
list_0 = [list_0[i] for i in randindex]

randindex = np.random.permutation(len(list_1))
randindex = randindex[0:cnt_1]
list_1 = [list_1[i] for i in randindex]

randindex = np.random.permutation(len(list_2))
randindex = randindex[0:cnt_2]
# pos = math.floor(args.ratio2 * len(list_2))
# randindex = randindex[:pos]
list_2 = [list_2[i] for i in randindex]

randindex = np.random.permutation(len(list_3))
randindex = randindex[0:cnt_3]
list_3 = [list_3[i] for i in randindex]

randindex = np.random.permutation(len(list_4))
randindex = randindex[0:cnt_4]
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

# csv_root = './screen_flag_1226_add_weight'
csv_root = args.output
os.makedirs(csv_root, exist_ok=True)

csv_data = os.path.join(csv_root, 'a_data_multi.csv')
csv_train = os.path.join(csv_root, 'a_train_multi.csv')
csv_val = os.path.join(csv_root, 'a_val_multi.csv')
csv_test = os.path.join(csv_root, 'a_test_multi.csv')

data_df.to_csv(csv_data)
train_df.to_csv(csv_train)
val_df.to_csv(csv_val)
test_df.to_csv(csv_test)


root_b = '/media/weidong/weidong/12.15质检图片'
sub_dirs = ['sort1', 'sort2', 'sort3', 'sort4', 'sort51', 'sort52']
b_list_0 = []
b_list_1 = []
b_list_2 = []
b_list_3 = []
b_list_4 = []
for sub_dir in sub_dirs:
    tmp_dir = os.path.join(root_b, sub_dir)
    for i in range(5):
        level_dir = os.path.join(tmp_dir, str(i))
        tmp_list = glob(os.path.join(level_dir,'*.jpg'))
        tmp_list = [os.path.basename(image_file).split('.')[0] for image_file in tmp_list]
        if i == 0:
            b_list_0 += tmp_list
        elif i == 1:
            b_list_1 += tmp_list
        elif i == 2:
            b_list_2 += tmp_list
        elif i == 3:
            b_list_3 += tmp_list
        elif i == 4:
            b_list_4 += tmp_list
randindex = np.random.permutation(len(b_list_0))
randindex = randindex[0:cnt_0]
b_list_0 = [b_list_0[i] for i in randindex]

randindex = np.random.permutation(len(b_list_1))
randindex = randindex[0:cnt_1]
b_list_1 = [b_list_1[i] for i in randindex]

randindex = np.random.permutation(len(b_list_2))
randindex = randindex[0:cnt_2]
b_list_2 = [b_list_2[i] for i in randindex]

randindex = np.random.permutation(len(b_list_3))
randindex = randindex[0:cnt_3]
b_list_3 = [b_list_3[i] for i in randindex]

randindex = np.random.permutation(len(b_list_4))
randindex = randindex[0:cnt_4]
b_list_4 = [b_list_4[i] for i in randindex]

b_dr_level = []
b_image_list = []

for i in range(len(b_list_0)):
    b_dr_level.append(0)
    b_image_list.append(b_list_0[i])

for i in range(len(b_list_1)):
    b_dr_level.append(1)
    b_image_list.append(b_list_1[i])
for i in range(len(b_list_2)):
    b_dr_level.append(2)
    b_image_list.append(b_list_2[i])
for i in range(len(b_list_3)):
    b_dr_level.append(3)
    b_image_list.append(b_list_3[i])
for i in range(len(b_list_4)):
    b_dr_level.append(4)
    b_image_list.append(b_list_4[i])

# b_image_list = [os.path.basename(i).split('.')[0] for i in b_image_list]

b_dme_level = []
b_referable_level = []

for i, dr in enumerate(b_dr_level):
    dme = dr if dr < 4 else 3
    b_dme_level.append(dme)
    ref = 0 if dr < 2 else 1
    b_referable_level.append(ref)

assert len(b_image_list) == len(b_dr_level) == len(b_dme_level) == len(b_referable_level)

# random
randindex = np.random.permutation(len(b_image_list))
b_image_list = [b_image_list[i] for i in randindex]
b_dr_level = [b_dr_level[i] for i in randindex]
b_dme_level = [b_dme_level[i] for i in randindex]
b_referable_level = [b_referable_level[i] for i in randindex]


test_ratio = 0.2
val_ratio = 0.1

b_data = np.column_stack((b_image_list, b_dr_level, b_dme_level, b_referable_level))

train_data, test_data = train_test_split(b_data, test_size=test_ratio)
train_data, val_data = train_test_split(train_data, test_size=val_ratio)

data_df = pd.DataFrame(b_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
train_df = pd.DataFrame(train_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
val_df = pd.DataFrame(val_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
test_df = pd.DataFrame(test_data, columns=['image', 'dr_level', 'dme_level', 'referable'])

# csv_root = './screen_flag_1226_add_weight'
csv_root = args.output
os.makedirs(csv_root, exist_ok=True)

csv_data = os.path.join(csv_root, 'b_data_multi.csv')
csv_train = os.path.join(csv_root, 'b_train_multi.csv')
csv_val = os.path.join(csv_root, 'b_val_multi.csv')
csv_test = os.path.join(csv_root, 'b_test_multi.csv')

data_df.to_csv(csv_data)
train_df.to_csv(csv_train)
val_df.to_csv(csv_val)
test_df.to_csv(csv_test)


sum_image_list = image_list + b_image_list
sum_dr_level = dr_level + b_dr_level
sum_dme_level = dme_level + b_dme_level
sum_referable_level = referable_level + b_referable_level

randindex = np.random.permutation(len(sum_image_list))
sum_image_list = [sum_image_list[i] for i in randindex]
sum_dr_level = [sum_dr_level[i] for i in randindex]
sum_dme_level = [sum_dme_level[i] for i in randindex]
sum_referable_level = [sum_referable_level[i] for i in randindex]

test_ratio = 0.2
val_ratio = 0.1

sum_data = np.column_stack((sum_image_list, sum_dr_level, sum_dme_level, sum_referable_level))

train_data, test_data = train_test_split(sum_data, test_size=test_ratio)
train_data, val_data = train_test_split(train_data, test_size=val_ratio)

data_df = pd.DataFrame(sum_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
train_df = pd.DataFrame(train_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
val_df = pd.DataFrame(val_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
test_df = pd.DataFrame(test_data, columns=['image', 'dr_level', 'dme_level', 'referable'])

# csv_root = './screen_flag_1226_add_weight'
csv_root = args.output
os.makedirs(csv_root, exist_ok=True)

csv_data = os.path.join(csv_root, 'data_multi.csv')
csv_train = os.path.join(csv_root, 'train_multi.csv')
csv_val = os.path.join(csv_root, 'val_multi.csv')
csv_test = os.path.join(csv_root, 'test_multi.csv')

data_df.to_csv(csv_data)
train_df.to_csv(csv_train)
val_df.to_csv(csv_val)
test_df.to_csv(csv_test)
