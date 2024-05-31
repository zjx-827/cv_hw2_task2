import sys
import os
import json
import xml.etree.ElementTree as ET

START_BOUNDING_BOX_ID = 0  # 起始的边界框ID

# 预定义的类别及其ID
PRE_DEFINE_CATEGORIES = {
    "aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4, "bottle": 5,
    "bus": 6, "car": 7, "cat": 8, "chair": 9, "cow": 10,
    "diningtable": 11, "dog": 12, "horse": 13, "motorbike": 14, "person": 15,
    "pottedplant": 16, "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20
}

# ID2CATEGORIES = {
#     1: "aeroplane", 2: "bicycle", 3: "bird", 4: "boat", 5: "bottle",
#     6: "bus", 7: "car", 8: "cat", 9: "chair", 10: "cow",
#     11: "diningtable", 12: "dog", 13: "horse", 14: "motorbike", 15: "person",
#     16: "pottedplant", 17: "sheep", 18: "sofa", 19: "train", 20: "tvmonitor"
# }


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError(f'无法在{root.tag}中找到{name}.')
    if 0 < length != len(vars):
        raise NotImplementedError(f'{name}的数量应该是{length}，但实际是{len(vars)}.')
    if length == 1:
        vars = vars[0]
    return vars


def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return filename
    except:
        raise NotImplementedError(f'文件名{filename}应是整数.')


def convert(xml_list, xml_dir, json_file):
    """
    Args:
        xml_list: xml文件存放的txt文件名
        xml_dir: 真实xml的存放路径
        json_file: 存放的json路径
    """
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID  # 起始的边界框ID
    with open(xml_list, 'r', encoding='utf-8') as f:
        list_fp = f.readlines()
    for line in list_fp:
        line = line.strip() + ".xml"
        print(f"处理文件 {line}")
        tree = ET.parse(os.path.join(xml_dir, line))
        root = tree.getroot()

        path = get(root, 'path')
        if len(path) == 1:
            filename = os.path.basename(path[0].text)  # 从路径中提取文件名
        elif len(path) == 0:
            filename = get_and_check(root, 'filename', 1).text  # 从filename标签中提取文件名
        else:
            raise NotImplementedError(f'{line}中找到{len(path)}个路径')

        image_id = get_filename_as_int(filename)
        # 获取图像的尺寸信息
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        objects = get(root, 'object')
        json_dict['images'].append({'file_name': filename, 'height': height, 'width': width, 'id': image_id})
        # 遍历所有object节点
        for obj in objects:
            category = get_and_check(obj, 'name', 1).text
            if category not in categories:
                new_id = len(categories) + 1
                categories[category] = new_id  # 为新的类别分配ID
            category_id = categories[category]
            # 获取边界框信息
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert xmax > xmin, f'{line}中的xmax应大于xmin'
            assert ymax > ymin, f'{line}中的ymax应大于ymin'
            o_width, o_height = xmax - xmin, ymax - ymin
            json_dict['annotations'].append({'area': o_width * o_height, 'bbox': [xmin, ymin, o_width, o_height],
                                             'image_id': image_id, 'category_id': category_id, 'id': bnd_id,
                                             'iscrowd': 0, 'ignore': 0, 'segmentation': []})
            bnd_id += 1  # 增加边界框ID

    for cate, cid in categories.items():
        json_dict['categories'].append({'supercategory': 'none', 'id': cid, 'name': cate})

    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_dict))


if __name__ == '__main__':
    from PIL import Image

    year = '2012'

    xml_dir = f'./data/VOCdevkit/VOC{year}/Annotations'

    data_name = 'trainval'  # 'train' | 'test' | 'val' | 'trainval'

    xml_list = f'./data/VOCdevkit/VOC{year}/ImageSets/Main/{data_name}.txt'
    json_dir = f'./data/COCO{year}/annotations/{data_name}.json'

    # convert(xml_list, xml_dir, json_dir)
    total_num = {}
    print(len(json.load(open(json_dir, 'r'))['images']))
    annotations = json.load(open(json_dir, 'r'))['annotations']
    print(len(annotations))

    # for ann in annotations:
    #     print(ID2CATEGORIES[ann['category_id']])
    #     print(ann)
    #     image_path = f'./data/VOCdevkit/VOC{year}/JPEGImages/' + ann["image_id"] + '.jpg'
    #     image = Image.open(image_path)
    #     image.show()
    #     input()
    #     # num = total_num.get(ann['category_id'], 0)
    #     # total_num[ann['category_id']] = num + 1
    # print(total_num)
