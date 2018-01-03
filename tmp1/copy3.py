import xlrd
import os
import shutil

root = '/media/weidong/weidong/12.15质检图片'
xls_file = os.path.join(root, '3_分级2017.05.01_2017.12.01.xls')
print(xls_file)

data = xlrd.open_workbook(xls_file)

table = data.sheets()[0] # 这里的0为几个tab页，也可以通过名字直接读取

dst_root_dir = os.path.join(root, 'sort3')
os.makedirs(dst_root_dir, exist_ok=True)
for i in range(5):
    tmp_dir = os.path.join(dst_root_dir, str(i))
    os.makedirs(tmp_dir,exist_ok=True)

src_root_dir = os.path.join(root, '3/Save')

nrows = table.nrows     # 表的行，第0行为列的标签


# 第0行为列的标签，因此从第1行开始读取，row[0]不是index，不要混淆
for i in range(1, nrows):
    try:
        row = table.row_values(i)
        name = str(int(row[0]))
        level = str(int(row[4]))
        src_file = os.path.join(src_root_dir, name+'.jpg')
        if not os.path.isfile(src_file):
            src_file = os.path.join(src_root_dir, name + '.jpeg')
        dst_file = os.path.join(dst_root_dir, '{}/{}.jpg'.format(level, name))
        shutil.copy(src_file, dst_file)
        print('====> copy from {} to {}'.format(src_file, dst_file))
    except:
        continue


print('hello world')