import argparse
import os
from os import listdir
from os.path import isfile
from PIL import Image

parser = argparse.ArgumentParser( description='converts a folder of jpg image to png')
parser.add_argument('foldername', metavar='foldername', type=str,
	help='jpg folder')
args = parser.parse_args()

foldername = args.foldername
cwd = os.getcwd()
folder = os.path.join(cwd,foldername)

out_folder = os.path.join(cwd,'png_images')
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

for f in listdir(folder):
	name, extension = f.split('.')
	if(extension=='jpg'):
		jpg = Image.open(os.path.join(folder,f))
		jpg.save(os.path.join(out_folder,name+'.png'))