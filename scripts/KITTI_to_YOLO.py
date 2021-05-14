import argparse
import os
import cv2
import random
from tqdm import tqdm

parser = argparse.ArgumentParser( description='Converts KITTI file to the YOLO format.')
parser.add_argument('train_folder', metavar='train_folder', type=str,
	help='folder containing images and labels folders')
parser.add_argument("out_folder", help="output folder")

args = parser.parse_args()

cwd = os.getcwd()
train_folder = os.path.join(cwd, args.train_folder)
images_folder = os.path.join(train_folder, "images")
labels_folder = os.path.join(train_folder, "labels")
out_folder = os.path.join(cwd, args.out_folder)
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

classes = ["noctuidae",
"geometridae",
"coleoptera",
"diptera",
"odonata",
"orthoptera",
"hemiptera",
"hymenoptera",
"trichoptera"]

files = [f for f in os.listdir(labels_folder) if os.path.isfile(os.path.join(labels_folder, f))]
random.shuffle(files)
for filename in tqdm(files):
	with open(os.path.join(labels_folder,filename),'r') as f:
		for line in f:
			elements = line.split()
			if len(elements) > 15:
				[label,_,_,_,xmin,ymin,xmax,ymax,_,_,_,_,_,_,_,prediction] =  elements
			else:
				[label,_,_,_,xmin,ymin,xmax,ymax,_,_,_,_,_,_,_] =  elements
			image_filename = filename.replace(".txt",".jpg")
			image_path = os.path.join(images_folder,image_filename)
			image = cv2.imread(image_path)
			h, w, c = image.shape
			x = (float(xmin)+(float(xmax)-float(xmin))/2)/w
			y = (float(ymin)+(float(ymax)-float(ymin))/2)/h
			width = (float(xmax)-float(xmin))/w
			height = (float(ymax)-float(ymin))/h
			if len(elements) > 15:
				out_line = str(classes.index(label))+" "+confidence+" "+str(x)+" "+str(y)+" "+str(width)+" "+str(height)
			else:
				out_line = str(classes.index(label))+" "+str(x)+" "+str(y)+" "+str(width)+" "+str(height)
			out_file = os.path.join(out_folder, filename)
			with open(out_file, 'w') as o:
				o.write(out_line)
