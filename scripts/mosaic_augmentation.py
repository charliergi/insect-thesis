import cv2
import numpy as np
import random
import os
import argparse
import math
from shutil import copy2

random.seed(42)

parser = argparse.ArgumentParser()
parser.add_argument("data_folder", help="folder containing both the image and labels folders")
parser.add_argument("out_folder", help="output folder")
args = parser.parse_args()

cwd = os.getcwd()
data_folder = os.path.join(cwd, args.data_folder)
images_folder = os.path.join(data_folder, "images")
labels_folder = os.path.join(data_folder, "labels")
out_folder = os.path.join(cwd, args.out_folder)
if not os.path.exists(out_folder):
    os.makedirs(out_folder)
out_images = os.path.join(out_folder, "images")
if not os.path.exists(out_images):
    os.makedirs(out_images)
out_labels = os.path.join(out_folder, "labels")
if not os.path.exists(out_labels):
    os.makedirs(out_labels)
script_path = os.path.abspath(os.path.dirname(__file__))
background_path = os.path.join(script_path,"mosaic_augmentation.jpg")

def count_lines(filename):
	with open(filename,"r") as f:
		i = 0
		for i, l in enumerate(f, 1):
			pass
	return i

def mosaic(images, labels_path):
	columns = math.ceil(math.sqrt(len(images)))
	X = np.empty(len(images), dtype=int)
	Y = np.empty(len(images), dtype=int)
	out_labels = []
	for num, img in enumerate(images):
		col = num%columns
		row = num/columns
		if col == 0:
			if num == 0:
				newX = random.randint(0,100)
				newY = random.randint(0,100) 
			else:
				newX = X[num-columns] + random.randint(-100,100)
				newY = Y[num-columns] + random.randint(412,612) 
		else:
			newX = X[num-1] + random.randint(412,612)
			newY = Y[num-1] + random.randint(-100,100)
		newX = max(412*col, newX)
		newX = min(612*col, newX)
		X[num] = newX
		newY = max(412*row, newY)
		newY = min(612*row, newY)
		Y[num] = newY 
		with open(label_paths[num], 'r') as f:
			for i, lbl in enumerate(f):
				label,_,_,_,minx,miny,maxx,maxy,_,_,_,_,_,_,_=lbl.split()
				minx = str( float(minx) + newX )
				maxx = str( float(maxx) + newX )
				miny = str( float(miny) + newY )
				maxy = str( float(maxy) + newY )
				out_line = label+" 0.0 0 0 "+minx+" "+miny+" "+maxx+" "+maxy+" 0 0 0 0 0 0 0"
				out_labels.append(out_line)

	size_x = math.ceil(X.max()) + 512
	size_y = math.ceil(Y.max()) + 512
	max_size = max(size_x, size_y)
	res = cv2.imread(background_path)
	res = res[0:max_size,0:max_size]
	for num, img in enumerate(images):
		startX = X[num]
		endX = startX+512
		startY = Y[num]
		endY = startY+512
		res[startY:endY,startX:endX] = img
	return res, out_labels

images_to_merge = random.randint(1,9)
images = []
label_paths = []
files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]
random.shuffle(files)
for f in files:
	in_img = os.path.join(images_folder,f)
	img = cv2.imread(in_img)
	out_img = os.path.join(out_images, f)
	label_filename = f.replace(".jpg",".txt")
	label_path = os.path.join(labels_folder,label_filename)
	out_lbl = os.path.join(out_labels, label_filename)
	number_objects = count_lines(label_path)
	if number_objects > 2 :
		cv2.imwrite(out_img, img)
		copy2(label_path, out_lbl)
	else:
		images.append(img)
		label_paths.append(label_path)
		if len(images) == images_to_merge:
			img, lbls= mosaic(images, label_paths)
			cv2.imwrite(out_img, img)
			with open(out_lbl, 'w') as filehandle:
				for lbl in lbls:
					filehandle.write('%s\n' % lbl)
			images_to_merge = random.randint(1,6)
			images = []
			label_paths = []
			#TODO: labels
if images:
	img, lbls = mosaic(images, label_paths)
	out_img = os.path.join(out_images, f)
	cv2.imwrite(out_img, img)
	with open(out_lbl, 'w') as filehandle:
		for lbl in lbls:
			filehandle.write('%s\n' % lbl)
