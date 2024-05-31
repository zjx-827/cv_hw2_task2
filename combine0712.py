import os
import shutil

# # 定义数据集的路径
# coco2007_path = './data/COCO2007/images/trainval'
# coco2012_path = './data/COCO2012/images/trainval'
# coco0712_path = './data/COCO0712/images/trainval'
#
# # 如果目标文件夹不存在，则创建它
# if not os.path.exists(coco0712_path):
#     os.makedirs(coco0712_path)
#
# # 获取COCO2007和COCO2012目录下所有的文件名
# coco2007_images = os.listdir(coco2007_path)
# coco2012_images = os.listdir(coco2012_path)
#
#
# # 定义一个函数用于拷贝图片
# def copy_images(src_folder, images_list, dst_folder):
#     for image_name in images_list:
#         src_image_path = os.path.join(src_folder, image_name)
#         dst_image_path = os.path.join(dst_folder, image_name)
#         if os.path.exists(src_image_path):
#             shutil.copyfile(src_image_path, dst_image_path)
#
#
# # 拷贝COCO2007的图片到COCO0712
# copy_images(coco2007_path, coco2007_images, coco0712_path)
#
# # 拷贝COCO2012的图片到COCO0712
# copy_images(coco2012_path, coco2012_images, coco0712_path)
#
# print("images 合并完成")


import json


def merge_coco_json(json1_path, json2_path, output_path):
    with open(json1_path, 'r') as f:
        coco1 = json.load(f)
    with open(json2_path, 'r') as f:
        coco2 = json.load(f)

    # 合并images和annotations
    images = coco1['images'] + coco2['images']
    annotations = coco1['annotations']
    ann_id = max(ann['id'] for ann in annotations) + 1

    for ann in coco2['annotations']:
        ann['id'] = ann_id
        annotations.append(ann)
        ann_id += 1

    # categories通常不变
    categories = coco1['categories']

    # 创建合并后的COCO字典
    merged_coco = {
        "images": images,
        "type": "instances",
        "annotations": annotations,
        "categories": categories
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(merged_coco))

    print("annotations 合并完成")


# 路径设置
json2007_trainval_path = './data/COCO2007/annotations/trainval.json'
json2012_trainval_path = './data/COCO2012/annotations/trainval.json'
merged_trainval_path = './data/COCO0712/annotations/trainval.json'

# 合并两个trainval JSON文件
merge_coco_json(json2007_trainval_path, json2012_trainval_path, merged_trainval_path)
