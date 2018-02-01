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
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description='weight')
    parser.add_argument('--ratio2', default=0.5, type=float)
    parser.add_argument('--output')
    return parser.parse_args()

args = parse_args()


'''

add weight for "ground truth==4" but "predict==0"

'''


# root_0 = '/home/weidong/data/sort_image/pure'
root_0 = '/media/weidong/weidong/test_a/0'
root_other = '/home/weidong/data/LabelImages'

list_0 = glob(os.path.join(root_0, '*.jpg'))

cnt_0 = len(list_0)
cnt_1 = int(cnt_0/65.2*2.4)
cnt_2 = int(cnt_0/65.2*21.9)
cnt_3 = int(cnt_0/65.2*4.1)
cnt_4 = int(cnt_0/65.2*6.3)


list_1 = glob(os.path.join(root_other, '1/*.jpg'))
list_2 = glob(os.path.join(root_other, '2/*.jpg'))
list_3 = glob(os.path.join(root_other, '3/*.jpg'))
list_4 = glob(os.path.join(root_other, '4/*.jpg'))


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


# copy
out_dir = '/media/weidong/weidong/test_a/all'
os.makedirs(out_dir, exist_ok=True)
for index in image_list:
    basename = os.path.basename(index)
    src_file = index
    dst_file = os.path.join(out_dir, basename)
    shutil.copy(src_file, dst_file)
    print('====> copy from {} to {}'.format(src_file, dst_file))


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
# csv_root = args.output
csv_root = '/media/weidong/weidong/test_a/all_flag'
os.makedirs(csv_root, exist_ok=True)

csv_data = os.path.join(csv_root, 'a_data_multi.csv')
csv_train = os.path.join(csv_root, 'a_train_multi.csv')
csv_val = os.path.join(csv_root, 'a_val_multi.csv')
csv_test = os.path.join(csv_root, 'a_test_multi.csv')

data_df.to_csv(csv_data)
train_df.to_csv(csv_train)
val_df.to_csv(csv_val)
test_df.to_csv(csv_test)
