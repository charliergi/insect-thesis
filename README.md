# insect-thesis

Welcome in the insect wildlife monitoring github repository of Simon Hick and Gilles Charlier. This repo contains all our script used during our master thesis in computer science in UCLouvain (2020-2021).
This repo contains multiple folders. Below we will explain briefly each one of them. You will find Readme.md files in each of these folders where you will find additional informations about dependencies and how to use them. 

## Installation
First let's update submodules: 

In our thesis, we decided to use the transfer learning toolkit from NVIDIA. This toolkit gives us the ability to run object detection models and switch easily between them as long as they use the same data format. To use TLT, we used Docker and an image from NGC. 
For more infos about this, please visit TLT introduction and documentation website : https://developer.nvidia.com/transfer-learning-toolkit as well as the NGC pretrained image link : https://ngc.nvidia.com/catalog/models/nvidia:tlt_pretrained_object_detection.

Once prerequisites have been installed, you can start using Docker.
We used this command to download, run the image and mount the folder containing this repository :

```
sudo docker run --runtime=nvidia -it -v /path/to/folder/containing/this/repo:/workspace/tlt-experiments -p 8888:8888 nvcr.io/nvidia/tlt-streamanalytics:v3.0-dp-py3

```


## annotate-to-KITTI
This folder is a fork of SaiPrajwal95's repository. This folder is used to annotate images as fast as possible. The main improvement over the original repo is the ability to review images that are already annotated. This speed up the annotation process when a algorithm (like Faster RCNN) pre-annotate images.

## augment
Mainly used as offline augmentation for testing purpose, this repository contains notebooks and specification files used to rotate, zoom, change colors and sharpness of our images. These scripts are not used for the moment.

## data
This folder contains all the datasets used in the training process of recognition algorithm. 

## faster_rcnn-notebooks 
This folder contains notebooks used to run Faster RCNN model with Transfer Learning Toolkit from NVIDIA. This whole 
