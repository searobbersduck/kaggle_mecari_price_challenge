import os
import pandas as pd
import shutil

root_0 = '/home/weidong/data/sort_image/NormalData'
root_pred_0 = '/home/weidong/data/sort_image/pred0'

res_csv = '/home/weidong/data/sort_image/NormalData/result.csv'

os.makedirs(root_pred_0, exist_ok=True)

df = pd.DataFrame.from_csv(res_csv)

for index, row in df.iterrows():
    src = os.path.join(root_0, row['image'])
    dst = os.path.join(root_pred_0, row['image'])
    if row['dr_level'] != 0:
        continue
    try:
        shutil.move(src, dst)
        print('====> copy from {} to {}'.format(src, dst))
    except:
        continue