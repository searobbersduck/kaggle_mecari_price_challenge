import xlrd
import os
import shutil
import pandas as pd
import numpy as np
from utils import quadratic_weighted_kappa, kappa_confusion_matrix, AverageMeter
from sklearn.metrics import confusion_matrix

root = '/media/weidong/weidong/12.15质检图片'
xls_file = os.path.join(root, '1_分级2017.05.01_2017.12.01.xls')
pred_csv = os.path.join(root, '1/result.csv')
print(xls_file)

data = xlrd.open_workbook(xls_file)

table = data.sheets()[0]

nrows = table.nrows

dict_gt = {}

for i in range(1, nrows):
    try:
        row = table.row_values(i)
        name = str(int(row[0]))
        level = str(int(row[3]))
        dict_gt[name+'.jpg'] = int(row[3])
    except:
        continue

dict_pred = {}

df = pd.DataFrame.from_csv(pred_csv)
for index, row in df.iterrows():
    dict_pred[row['image']] = row['dr_level']

list_gt = []
list_pred = []

for key in dict_pred.keys():
    list_gt.append(dict_gt[key])
    list_pred.append(dict_pred[key])

np_gt = np.array(list_gt)
np_pred = np.array(list_pred)

dr_kappa = quadratic_weighted_kappa(np_gt, np_pred)

dr_confusion_matrix = str(confusion_matrix(np_gt, np_pred))

out_file = os.path.join(root, 'kappa1.txt')

with open(out_file, 'w') as f:
    f.write('====>kappa: {}\n'.format(dr_kappa))
    f.write('===> Confusion Matrix:\n')
    f.write(dr_confusion_matrix)
    f.write('\n\n')
