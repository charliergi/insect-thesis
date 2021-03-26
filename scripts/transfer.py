import sys
import os
from os import listdir, path
from os.path import isfile, join
import fileinput

# on veut que toutes les images qui n'ont pas de labels bougent dans inference/images
dataset_folder = sys.argv[1]
dataset_train_images_path = dataset_folder+"/train/images"
dataset_train_labels_path = dataset_folder+"/train/labels"
dataset_inference_images_path = dataset_folder+"/inference/images"


dataset_train_images = [f for f in listdir(dataset_train_images_path) if isfile(join(dataset_train_images_path, f))]
dataset_train_labels = [f for f in listdir(dataset_train_labels_path) if isfile(join(dataset_train_labels_path, f))]

for train_file in dataset_train_images:
    if not train_file.split("-")[0]+"-geometridae.txt" in dataset_train_labels:
        os.rename(dataset_train_images_path+"/"+train_file,dataset_inference_images_path+"/"+train_file)

