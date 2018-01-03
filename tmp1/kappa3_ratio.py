import xlrd
import os
import shutil
import pandas as pd
import numpy as np
from utils import quadratic_weighted_kappa, kappa_confusion_matrix, AverageMeter
from sklearn.metrics import confusion_matrix
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='kappa3_ratio')
    parser.add_argument('--csvfile', required=True)
    parser.add_argument('--error_output', required=True)
    return parser.parse_args()

args = parse_args()

root = '/media/weidong/weidong/12.15质检图片'
xls_file = os.path.join(root, '3_分级2017.05.01_2017.12.01.xls')
# pred_csv = os.path.join(root, '3/Save/result.csv')
pred_csv = os.path.join(root, args.csvfile)
print(xls_file)

data = xlrd.open_workbook(xls_file)

table = data.sheets()[0]

nrows = table.nrows

dict_gt = {}

for i in range(1, nrows):
    try:
        row = table.row_values(i)
        name = str(int(row[0]))
        level = str(int(row[4]))
        dict_gt[name+'.jpg'] = int(row[4])
    except:
        continue

dict_pred = {}

df = pd.DataFrame.from_csv(pred_csv)
for index, row in df.iterrows():
    dict_pred[row['image']] = row['dr_level']

list_gt = []
list_pred = []

# make dir
root_error = os.path.join(root, args.error_output)
os.makedirs(root_error, exist_ok=True)
for i in range(5):
    for j in range(5):
        tmp_dir = os.path.join(root_error, 'gt_{}_pred_{}'.format(i, j))
        os.makedirs(tmp_dir, exist_ok=True)


for key in dict_pred.keys():
    list_gt.append(dict_gt[key])
    list_pred.append(dict_pred[key])
    if (dict_gt[key] != dict_pred[key]):
        src_file = os.path.join(root, '3/Save/{}'.format(key))
        dst_file = os.path.join(root_error, 'gt_{}_pred_{}'.format(dict_gt[key], dict_pred[key]))
        shutil.copy(src_file, dst_file)
        print('copy from {} to {}'.format(src_file, dst_file))

print(len(list_pred))
print(len(list_gt))

np_gt = np.array(list_gt)
np_pred = np.array(list_pred)

dr_kappa = quadratic_weighted_kappa(np_gt, np_pred)

dr_confusion_matrix = str(confusion_matrix(np_gt, np_pred))

out_file = os.path.join(root, 'kappa3.txt')

with open(out_file, 'w') as f:
    f.write('====>kappa: {}\n'.format(dr_kappa))
    f.write('===> Confusion Matrix:\n')
    f.write(dr_confusion_matrix)
    f.write('\n\n')
