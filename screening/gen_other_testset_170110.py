# import pandas as pd
# import os
# from glob import glob
# import numpy as np
# import shutil
#
# csv_file = 'xxx/b_data_multi.csv'
# df_train = pd.DataFrame.from_csv(csv_file)
# df_train['image'] = df_train['image'].apply(lambda s:str(s))
#
# root_b = '/media/weidong/weidong/12.15质检图片'
# sub_dirs = ['sort1', 'sort2', 'sort3', 'sort4', 'sort51', 'sort52']
# b_list_0 = []
# b_list_1 = []
# b_list_2 = []
# b_list_3 = []
# b_list_4 = []
# for sub_dir in sub_dirs:
#     tmp_dir = os.path.join(root_b, sub_dir)
#     for i in range(5):
#         level_dir = os.path.join(tmp_dir, str(i))
#         tmp_list = glob(os.path.join(level_dir,'*.jpg'))
#         tmp_list = [os.path.basename(image_file).split('.')[0] for image_file in tmp_list]
#         if i == 0:
#             b_list_0 += tmp_list
#         elif i == 1:
#             b_list_1 += tmp_list
#         elif i == 2:
#             b_list_2 += tmp_list
#         elif i == 3:
#             b_list_3 += tmp_list
#         elif i == 4:
#             b_list_4 += tmp_list
# randindex = np.random.permutation(len(b_list_0))
# b_list_0 = [b_list_0[i] for i in randindex]
#
# randindex = np.random.permutation(len(b_list_1))
# b_list_1 = [b_list_1[i] for i in randindex]
#
# randindex = np.random.permutation(len(b_list_2))
# b_list_2 = [b_list_2[i] for i in randindex]
#
# randindex = np.random.permutation(len(b_list_3))
# b_list_3 = [b_list_3[i] for i in randindex]
#
# randindex = np.random.permutation(len(b_list_4))
# b_list_4 = [b_list_4[i] for i in randindex]
#
# b_dr_level = []
# b_image_list = []
#
# for i in range(len(b_list_0)):
#     b_dr_level.append(0)
#     b_image_list.append(b_list_0[i])
#
# for i in range(len(b_list_1)):
#     b_dr_level.append(1)
#     b_image_list.append(b_list_1[i])
# for i in range(len(b_list_2)):
#     b_dr_level.append(2)
#     b_image_list.append(b_list_2[i])
# for i in range(len(b_list_3)):
#     b_dr_level.append(3)
#     b_image_list.append(b_list_3[i])
# for i in range(len(b_list_4)):
#     b_dr_level.append(4)
#     b_image_list.append(b_list_4[i])
#
# b_dme_level = []
# b_referable_level = []
#
# for i, dr in enumerate(b_dr_level):
#     dme = dr if dr < 4 else 3
#     b_dme_level.append(dme)
#     ref = 0 if dr < 2 else 1
#     b_referable_level.append(ref)
#
# assert len(b_image_list) == len(b_dr_level) == len(b_dme_level) == len(b_referable_level)
#
# b_data = np.column_stack((b_image_list, b_dr_level, b_dme_level, b_referable_level))
#
# b_data_df = pd.DataFrame(b_data, columns=['image', 'dr_level', 'dme_level', 'referable'])
#
# other_data_df = b_data_df[~b_data_df['image'].isin(df_train['image'])]
#
# all_folder = os.path.join(root_b, 'all1')
# other_folder = os.path.join(root_b, 'other')
# os.makedirs(other_folder, exist_ok=True)
#
# # for index, row in other_data_df.iterrows():
# #     image_name = str(row[0])
# #     src_file = os.path.join(all_folder, '{}.jpg'.format(image_name))
# #     dst_file = os.path.join(other_folder, '{}.jpg'.format(image_name))
# #     shutil.copy(src_file, dst_file)
# #     print('====> copy from {} to {}'.format(src_file, dst_file))
#
#
# other_data_df.to_csv(os.path.join(other_folder, 'ground_truth.csv'))
#
# print('hello world')


import pandas as pd
import os
import numpy as np
from sklearn.metrics import confusion_matrix
from utils import quadratic_weighted_kappa, kappa_confusion_matrix, AverageMeter
import shutil

root_b = '/media/weidong/weidong/12.15质检图片'
other_folder = os.path.join(root_b, 'other')
pred_csv = os.path.join(other_folder, 'result.csv')
gt_csv = os.path.join(other_folder, 'ground_truth.csv')
out_csv = os.path.join(other_folder, 'result_gt.csv')

df_pred = pd.DataFrame.from_csv(pred_csv)
df_gt = pd.DataFrame.from_csv(gt_csv)

list_gt = []
list_pred = []
for index, row in df_pred.iterrows():
    list_pred.append(row['dr_level'])
    tmp_level = df_gt.loc[df_gt['image'] == int(row['image'].split('.')[0])]['dr_level'].iloc[0]
    list_gt.append(tmp_level)

assert len(list_gt) == len(list_pred)

df_pred['gt'] = pd.Series(np.array(list_gt))

df_pred.to_csv(out_csv)

np_gt = np.array(list_gt)
np_pred = np.array(list_pred)
dr_confusion_matrix = str(confusion_matrix(np_gt, np_pred))
dr_kappa = quadratic_weighted_kappa(np_gt, np_pred)

out_file = os.path.join(other_folder, 'kappa.txt')

with open(out_file, 'w') as f:
    f.write('====>kappa: {}\n'.format(dr_kappa))
    f.write('===> Confusion Matrix:\n')
    f.write(dr_confusion_matrix)
    f.write('\n\n')

error_folder = os.path.join(other_folder, 'error')
os.makedirs(error_folder, exist_ok=True)
for i in range(5):
    for j in range(5):
        tmp_dir = os.path.join(error_folder, 'gt_{}_pred_{}'.format(i,j))
        os.makedirs(tmp_dir, exist_ok=True)

for index, row in df_pred.iterrows():
    image_file = row['image']
    src_file = os.path.join(other_folder, image_file)
    dst_file = os.path.join(error_folder, 'gt_{}_pred_{}/{}'.format(row['gt'], row['dr_level'], image_file))
    if row['gt'] == row['dr_level']:
        continue
    shutil.copy(src_file, dst_file)
    print('====> copy from {} to {}'.format(src_file, dst_file))


