import os
import shutil

# year = '2007'
# output_dir = ['test', 'trainval']

year = '2012'
output_dir = ['trainval']

images_file_path = f'./data/VOCdevkit/VOC{year}/JPEGImages/'
split_data_file_path = f'./data/VOCdevkit/VOC{year}/ImageSets/Main/'
new_images_file_path = f'./data/COCO{year}/images'

for folder in output_dir:
    folder_path = os.path.join(new_images_file_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 拷贝图片到对应文件夹
total_txt = os.listdir(split_data_file_path)
for txt_file_name in total_txt:
    # 提取文件名，去掉后缀
    name = os.path.splitext(txt_file_name)[0]
    if name in output_dir:
        dst_folder = name
    else:
        continue

    # 打开文件，逐行读取文件名，并拷贝图片
    with open(os.path.join(split_data_file_path, txt_file_name), 'r') as txt_file:
        for line in txt_file:
            line = line.strip('\n').strip('\r')
            # 构建源图片路径和目标图片路径
            src_image_path = os.path.join(images_file_path, line + '.jpg')
            dst_image_path = os.path.join(new_images_file_path, dst_folder, line + '.jpg')
            # 拷贝图片
            shutil.copyfile(src_image_path, dst_image_path)
