from mmdet.apis import DetInferencer
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

image_name = '000062' # '000001' | '000002' | '000010' | '000065' | '000062'
H, W = 608, 928  # 864, 608 | 896, 608 | 832, 608 | 608, 896 | 608, 928

# # 初始化模型
# inferencer = DetInferencer(model='work_dirs/1_faster-rcnn_r50_fpn_1x_voc/1_faster-rcnn_r50_fpn_1x_voc.py', weights='work_dirs/1_faster-rcnn_r50_fpn_1x_voc/epoch_12.pth', device='cuda:0')

# # 推理示例图片
# inferencer(f'data/VOCdevkit/VOC2007/JPEGImages/{image_name}.jpg', show=True, out_dir='outputs1/', no_save_pred=False)


# 加载保存的bboxes.npy文件
save_dir = 'test_demo/'
bboxes_path = os.path.join(save_dir, f'bboxes_{image_name}.npy')
bboxes = np.load(bboxes_path)

# 加载对应的图片
image_path = f'data/VOCdevkit/VOC2007/JPEGImages/{image_name}.jpg'  # 替换为你的图片路径
image = cv2.imread(image_path)
width, height = image.shape[1], image.shape[0]
print(width, height)

for bbox in bboxes:
    x1, y1, x2, y2 = bbox  # 取前四个坐标，最后一个元素为置信度，此处不用
    cv2.rectangle(image, (int(x1 / W * width), int(y1 / H * height)), (int(x2 / W * width), int(y2 / H * height)), (0, 255, 0), 2)
    print((int(x1 / W * width), int(y1 / H * height)), (int(x2 / W * width), int(y2 / H * height)))
print(width, height)

# # 显示图片
# img = np.ascontiguousarray(img)
# win_name = 'RPN_proposals'
# fig = plt.figure(win_name, frameon=False)
# plt.title(win_name)
# canvas = fig.canvas
# dpi = fig.get_dpi()
# print(dpi)
# # add a small EPS to avoid precision lost due to matplotlib's truncation
# # (https://github.com/matplotlib/matplotlib/issues/15363)
# EPS = 1e-2
# fig.set_size_inches((width + EPS) / dpi, (height + EPS) / dpi)

# # remove white edges by set subplot margin
# plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
# ax = plt.gca()
# ax.axis('off')
# 保存可视化后的图片
save_image_path = os.path.join(save_dir, f'visualized_image_{image_name}.jpg')
cv2.imwrite(save_image_path, image)
