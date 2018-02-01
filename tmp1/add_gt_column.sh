#!/usr/bin/env bash
# python add_gt_column.py --root /media/weidong/weidong/test_a --csvfile result.csv --error_output error --root_sub all --gt /media/weidong/weidong/test_a/all_flag/a_data_multi.csv

python add_gt_column.py --root /media/weidong/weidong/12.15质检图片/train_b --csvfile result.csv --error_output error --root_sub 0 --gt /media/weidong/weidong/12.15质检图片/train_b/b0_data_multi.csv

python add_gt_column.py --root /media/weidong/weidong/12.15质检图片/train_b --csvfile result.csv --error_output error --root_sub 1 --gt /media/weidong/weidong/12.15质检图片/train_b/b1_data_multi.csv

python add_gt_column.py --root /media/weidong/weidong/12.15质检图片/train_b --csvfile result.csv --error_output error --root_sub 2 --gt /media/weidong/weidong/12.15质检图片/train_b/b2_data_multi.csv
