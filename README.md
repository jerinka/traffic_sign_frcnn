# faster_rcnn_pytorch

Modified from KaggleFaceMaskDetection

## Introduction

This is a PyTorch project using Faster RCNN for 2-class face mask detection.

For Faster RCNN tutorial, please see: https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html

## Dataset Description

Kaggle face mask detection dataset: https://www.kaggle.com/andrewmvd/face-mask-detection

- contains 853 images
- each image is accompanied by an annotation file, including multiple bounding boxes and labels
- 3-classes annotation is available: with_mask, without_mask, mask_weared_incorrect (not used in this project)

## Folder Structure

FaceMaskDetection

|-- data  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- original_data  
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-- images  
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|-- annotations  
|-- utilities  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- coco_utils  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- data_utils  
|&nbsp;&nbsp;&nbsp;&nbsp;|-- train_eval  
|-- output  
|-- model  
README.md  
requirements.txt  
setup.py  
train.py  
test.py

## Env creation (one time)

```virtualenv venv3/bin/activate```

```source venv3/bin/activate```

```pip3 install -r requirements.txt```

## Activating env (every time u open terminal)

```source venv3/bin/activate```

## Data Preprocessing

Split images and labels into train and test folders maunally

- Add more images in train and some images to val (currently only very few)

## Train and Test

```python3 train.py```

- For training, please run train.py so to generate the model; or you can simply download the pre-trained model from: https://drive.google.com/drive/folders/1UuU5up0DQfRuafdbZrayPdRwpVvJOYYK?usp=sharing

```python3 test.py```

- the testing results will be written into the output folder, here's an example of prediction:![Example Output](https://github.com/adoskk/KaggleFaceMaskDetection/blob/master/output/result4.png)


