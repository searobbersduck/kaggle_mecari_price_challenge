import os
import pandas as pd
import shutil
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='parse args')
    parser.add_argument('--root', required=True)
    return parser.parse_args()

args = parse_args()

csv_file = os.path.join(args.root, 'result.csv')

df = pd.DataFrame.from_csv(csv_file)

dir_0 = os.path.join(args.root, '0')
dir_1 = os.path.join(args.root, '1')
os.makedirs(dir_0, exist_ok=True)
os.makedirs(dir_1, exist_ok=True)

for index, row in df.iterrows():
    image_name = row['image']
    src = os.path.join(args.root, image_name)
    if row['referable'] == 0:
        dst = os.path.join(dir_0, image_name)
    else:
        dst = os.path.join(dir_1, image_name)
    try:
        shutil.move(src, dst)
        print('====> move from {} to {}'.format(src, dst))
    except:
        continue