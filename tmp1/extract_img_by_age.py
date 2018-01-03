import argparse
from glob import glob
import os
import xlrd
import pandas as pd
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='parse according to age')
    parser.add_argument('--txtfile', default='id_age.txt')
    return parser.parse_args()

args = parse_args()

age_list = []

above_70 = []
above_60 = []
above_65 = []
above_55 = []

current = 2018

# with open(args.txtfile, 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         tmp_vec = line.strip().split('    ')
#         age = int(tmp_vec[1].split('-')[0])
#         age = current - age
#         age_list.append(tmp_vec[0])
#         if age >= 60:
#             above_60.append(tmp_vec[0])
#         if age >= 65:
#             above_65.append(tmp_vec[0])
#         if age >= 55:
#             above_55.append(tmp_vec[0])
#         if age >= 70:
#             above_70.append(tmp_vec[0])
#
# print('age >= 55: {}'.format(len(above_55)))
# print('age >= 60: {}'.format(len(above_60)))
# print('age >= 65: {}'.format(len(above_65)))
# print('age >= 70: {}'.format(len(above_70)))
# print('all image number: {}'.format(len(age_list)))

root = '/media/weidong/weidong/12.15质检图片'
flags = ['1_分级2017.05.01_2017.12.01.xls',
         '2_分级2017.05.01_2017.12.01.xls',
         '3_分级2017.05.01_2017.12.01.xls',
         '4_分级2017.05.01_2017.12.01.xls',
         '5_1_分级2017.05.01_2017.08.31.xls',
         '5_2_分级2017.09.01_2017.12.14.xls']
flags_list = []
flags_flatten_list = []

for flag in flags:
    xls_file = os.path.join(root, flag)
    data = xlrd.open_workbook(xls_file)
    table = data.sheets()[0]
    nrows = table.nrows
    tmp_list = []
    for i in range(1, nrows):
        row = table.row_values(i)
        name = str(int(row[0]))
        tmp_list.append(name)
        flags_flatten_list.append(name)
    flags_list.append(tmp_list)

print('====> step: ')

exist_list = []
exist_info = []
with open(args.txtfile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        tmp_vec = line.strip().split('    ')
        if tmp_vec[0] in flags_flatten_list:
            exist_list.append(tmp_vec[0])

            exist_info.append(tmp_vec)

print(len(exist_list))
print(len(flags_flatten_list))

arr = np.array(exist_info)
df = pd.DataFrame(arr)

df.to_csv(os.path.join(root, 'exist_info.csv'))



