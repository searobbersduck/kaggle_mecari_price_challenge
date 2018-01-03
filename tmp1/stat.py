import os
from glob import glob
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='stat zhizhen refined data')
    parser.add_argument('--root', default='/media/weidong/weidong/12.15质检图片')
    return parser.parse_args()

args = parse_args()

root = args.root

folders = ['sort1', 'sort2', 'sort3', 'sort4', 'sort51', 'sort52']

folders = [os.path.join(root, folder) for folder in folders]

def log_folder(folder_dir):
    logger = []
    cnt_list = []
    all_image_list = []
    logger.append('\n')
    logger.append('====> images in {} list as follows: '.format(folder_dir))
    total_cnt = 0
    for i in range(5):
        tmp_dir = os.path.join(folder_dir, str(i))
        image_list = glob(os.path.join(tmp_dir, '*.jpg'))
        image_list = [os.path.basename(i) for i in image_list]
        all_image_list += image_list
        total_cnt += len(image_list)
    for i in range(5):
        tmp_dir = os.path.join(folder_dir, str(i))
        image_list = glob(os.path.join(tmp_dir, '*.jpg'))
        cnt_list.append(len(image_list))
        logger.append('\n\t\tgraded level-{}: {}\t{:.1f}%'.format(i, len(image_list), len(image_list)/total_cnt*100))
    logger.append('\n')
    return logger, cnt_list, all_image_list

logger = []
cnt = [0]*5
image_list = []

for folder_dir in folders:
    logger_sub, cnt_sub, image_list_sub = log_folder(folder_dir)
    for log in logger_sub:
        logger.append(log)
    for i,c in enumerate(cnt_sub):
        cnt[i] += c
    image_list += image_list_sub

logger.append('\n')
total_cnt = 0
for c in cnt:
    total_cnt += c
logger.append('====> total images number is: {}. list as follows: '.format(total_cnt))
for i, c in enumerate(cnt):
    logger.append('\n\t\tgraded level-{}: {}\t{:.1f}%'.format(i, c, c / total_cnt*100))
logger.append('\n')


logger_file = os.path.join(root, 'logger.txt')
with open(logger_file, 'w') as f:
    for log in logger:
        f.write(log)


root_old= '/home/weidong/data'
root_old_normal = os.path.join(root_old, 'NormalData')
root_old_label = os.path.join(root_old, 'LabelImages')
normal_list = glob(os.path.join(root_old_normal, '*.jpg'))
normal_list = [os.path.basename(i).replace('NormalData','') for i in normal_list]
label_list = []
for i in range(1,5):
    list = glob(os.path.join(root_old_label, '{}/*.jpg'.format(i)))
    list = [os.path.basename(i) for i in list]
    label_list += list


duplicate_cnt_normal = 0
for i in image_list:
    if i in normal_list:
        duplicate_cnt_normal += 1


duplicate_cnt_label = 0
for i in image_list:
    if i in label_list:
        duplicate_cnt_label += 1


logger_a = []
logger_a.append('\n')
logger_a.append('====> duplicate in NormalData number is {}\n'.format(duplicate_cnt_normal))
logger_a.append('====> duplicate in LabelImages number is {}\n'.format(duplicate_cnt_label))
logger_a.append('\n')
with open(logger_file, 'a') as f:
    for log in logger_a:
        f.write(log)