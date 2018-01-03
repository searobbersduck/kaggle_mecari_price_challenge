root = '/media/weidong/weidong/12.15质检图片'

import pandas as pd
import os
from glob import glob
import shutil

csv_file = os.path.join(root, 'exist_info.csv')

df = pd.DataFrame.from_csv(csv_file)

image_list = []
image_list_70 = []
image_list_65 = []
image_list_60 = []
image_list_55 = []

current = 2018

for index,row in df.iterrows():
    age = int(row[1].split('-')[0])
    age = current - age
    image_list.append(row[0])
    if age >=  70:
        image_list_70.append(row[0])
    if age >= 65:
        image_list_65.append(row[0])
    if age >= 60:
        image_list_60.append(row[0])
    if age >= 55:
        image_list_55.append(row[0])

print(len(image_list_70))

folder_3_0 = os.path.join(root, 'sort3/0')
folder_3_0_list = glob(os.path.join(folder_3_0, '*.jpg'))
folder_3_0_list = [os.path.basename(i).split('.')[0] for i in folder_3_0_list]

copy_list = []

for index in image_list_70:
    if str(index) in folder_3_0_list:
        copy_list.append(str(index))

print(len(copy_list))

print('hello world')

age70_3dir = os.path.join(root, 'age70_3')
os.makedirs(age70_3dir, exist_ok=True)

for index in copy_list:
    src_file = os.path.join(folder_3_0, index+'.jpg')
    dst_file = os.path.join(age70_3dir, index+'.jpg')
    shutil.copy(src_file, dst_file)
    print('====>copy from {} to {}'.format(src_file, dst_file))

