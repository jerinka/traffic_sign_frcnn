import os
from utilities.data_utils.Dataset import FacialDataset, get_transform
from utilities.utils import collate_fn
from utilities.train_eval.engine import train_one_epoch, evaluate, get_model_result
import glob

import nvidia_smi # for python 3, you need nvidia-ml-py3 library

import torch
import torchvision

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator, RPNHead

PATH = 'Weight.pth'
output_image_folder = 'output'
num_classes = 3  # 2 class (person) + background
test_size = 80 # leave 80 images for testing


if __name__ == "__main__":
    
    torch.cuda.empty_cache()
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    print("Total memory:", info.total)
    print("Free memory:", info.free)
    print("Used memory:", info.used)
    
    dataset_test = FacialDataset('data/test', get_transform(horizontal_flip=False))
        
    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=0,
        collate_fn=collate_fn)
    
    
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    
    anchor_generator = AnchorGenerator(sizes=((32,), (24, ), (24, ), (16,), (8, )),
                                       aspect_ratios=([1.0, 1.0, 1.0, 1.0],
                                                      [0.8, 1.0, 1.0, 1.0],
                                                      [1.0, 0.8, 1.0, 1.0],
                                                      [1.0, 1.0, 1.0, 1.0],
                                                      [1.0, 1.0, 1.0, 1.0]))
    model.rpn.anchor_generator = anchor_generator
    model.rpn.head = RPNHead(256, anchor_generator.num_anchors_per_location()[0])
    # get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    model.load_state_dict(torch.load(PATH))
    model.to(device)

    # create output directory
    # if output directory exists, delete existing files
    if not os.path.exists(output_image_folder):
        os.mkdir(output_image_folder)
    else:
        files = glob.glob(output_image_folder + '/*')
        for f in files:
            os.remove(f)
    # write testing result to output folder
    for img_idx, batch_sampler in enumerate(data_loader_test):
        img_test = batch_sampler[0][0]
        target_test = batch_sampler[1][0]
        i = target_test["image_id"].item()
        get_model_result(img_test, model, target_test, i, device, location=output_image_folder, threshold=0.15)
    
    print("Testing complete!")
    
    torch.cuda.synchronize()
    nvidia_smi.nvmlShutdown()


            
