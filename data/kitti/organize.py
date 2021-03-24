import sys
import os
from os import listdir, path
from os.path import isfile, join
import fileinput

#This script has to be launcher in the root folder of KITTI datas
#give as argument the root of the dataset.
dataset_folder = sys.argv[1]
dataset_images = dataset_folder+"/images"
dataset_labels = dataset_folder+"/labels"

if not path.exists(dataset_folder+"/train") : os.mkdir(dataset_folder+"/train")
if not path.exists(dataset_folder+"/test") : os.mkdir(dataset_folder+"/test")
if not path.exists(dataset_folder+"/train/images") : os.mkdir(dataset_folder+"/train/images")
if not path.exists(dataset_folder+"/train/labels") : os.mkdir(dataset_folder+"/train/labels")
if not path.exists(dataset_folder+"/test/images") : os.mkdir(dataset_folder+"/test/images")


image_files = [f for f in listdir(dataset_images) if isfile(join(dataset_images, f))]
#if path.exists(dataset_folder+"/labels"):
label_files = [f for f in listdir(dataset_labels) if isfile(join(dataset_labels, f))]

for file in image_files:
    image_name = file.split(".")[0] #remove extension
    print(image_name)
    if image_name+".txt" in label_files:
        os.rename(dataset_folder+"/images/"+file, dataset_folder+"/train/images/"+file)
        os.rename(dataset_folder+"/labels/"+image_name+".txt", dataset_folder+"/train/labels/"+image_name+".txt")
        print("moving",dataset_folder+"/images/"+file, "into", dataset_folder+"/train/images/"+file)
    else:
        os.rename(dataset_folder+"/images/"+file, dataset_folder+"/test/images/"+file)

os.rmdir(dataset_folder+"/images")
os.rmdir(dataset_folder+"/labels")