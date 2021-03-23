import argparse
import os
from os import listdir
from os.path import isfile
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser( description='draw the label rectangle on the corresponding image')
parser.add_argument('image_folder', metavar='foldername', type=str,
	help='image folder')
parser.add_argument('label_folder', metavar='foldername', type=str,
	help='label folder')
args = parser.parse_args()
image_folder = args.image_folder
label_folder = args.label_folder

cwd = os.getcwd()
images = os.path.join(cwd,image_folder)

out_folder = os.path.join(cwd,'labelled_images')
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

for im in listdir(images):
	name, ext = im.split('.')
	label_file = os.path.join(cwd,label_folder,name+'.txt')
	image = Image.open(os.path.join(images,im))
	draw = ImageDraw.Draw(image)
	with open(label_file,'r') as l:
		for line in l:
			try:
				label, _, _, _, xmin, ymin, xmax, ymax, _, _ , _, _, _, _ , _= line.split(' ')
			except ValueError:
				print(line)
			else:
				draw.rectangle(((float(xmin), float(ymin)), (float(xmax), float(ymax))), outline="green")
	image.save(os.path.join(out_folder,im), ext)