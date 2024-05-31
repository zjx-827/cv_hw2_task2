# 实验目的

在VOC数据集上训练并测试目标检测模型Faster R-CNN和YOLO V3。


# 实验环境

本实验在ubuntu22.04上进行，Python选用3.9版本
环境创建过程（Anaconda）：
conda create -n mmdet_py39 python=3.9 anaconda
conda activate mmdet_py39
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
按照官方文档进行代码下载及依赖项配置：https://mmdetection.readthedocs.io/en/latest/get_started.html


# 实验数据

PASCAL VOC2007，PASCAL VOC2012

依次执行voc2coco.py、copy_image_to_coco.py和combine0712.py，将VOC类型数据转为COCO类型数据，并将2007和2012数据合并。

最终实验数据结果（data文件夹下）

```
VOCdevkit    VOC类型数据
    └── VOC2012
    │    ├── Annotations      所有的图像标注信息（XML文件）
    │    ├── ImageSets		
    │    │   ├── Main					    目标检测分类图像信息
    │    │   │     ├── train.txt  训练集(5717)
    │    │   │     ├── val.txt		验证集(5823)
    │    │   │     └── trainval.txt	训练集+验证集(11540)
    │    │   │
    │    │   └── …
    │    │ 
    │    ├── JPEGImages            所有图像文件
    │    ├── …
    └── VOC2007（与VOC2012结构相同）

COCO0712      COCO类型数据
     ├── trainval        所有训练图像文件夹
     ├── test            所有验证（测试）图像文件夹
     └── annotations     所有的图像标注信息（json文件）
```

