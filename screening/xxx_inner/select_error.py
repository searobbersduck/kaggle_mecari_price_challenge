import pandas as pd
import argparse
import os
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description='sellect error data from DR dataset')
    parser.add_argument('--root', required=True)
    parser.add_argument('--gt', required=True)
    return parser.parse_args()

args = parse_args()
root = args.root

error_dir = os.path.join(root, 'error')
os.makedirs(error_dir, exist_ok=True)

flag = [0,1,2,3,4]
for i in range(5):
    for j in range(5):
        dir_name = 'gt_{}_pred_{}'.format(i,j)
        dir = os.path.join(error_dir, dir_name)
        os.makedirs(dir, exist_ok=True)

csv_file = os.path.join(root, 'result.csv')
assert os.path.isfile(csv_file)


df_gt = pd.DataFrame.from_csv(args.gt)
df = pd.DataFrame.from_csv(csv_file)

for index, row in df.iterrows():
    gt_level = df_gt.loc[df_gt['image'] == int(row['image'].split('.')[0])]['dr_level'].iloc[0]
    pred_level = row['dr_level']
    if gt_level == pred_level:
        continue
    src_file = os.path.join(root, row['image'])
    dst_file = os.path.join(error_dir, 'gt_{}_pred_{}/{}'.format(gt_level, pred_level, row['image']))
    shutil.copy(src_file, dst_file)
    print('====> copy from {} to {}'.format(src_file, dst_file))
