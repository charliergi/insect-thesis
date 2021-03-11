import argparse
import os.path

parser = argparse.ArgumentParser(
parser.add_argument('csv_file')
args = parser.parse_args()

cwd = os.getcwd()

with open(csv_file, "r") as f:
    for line in f:
    	class_name, xmin, ymin, imagename, width, height = line.split(',')
    	filename, ext = imagename.split('.')
    	out_file = filename+".txt"
    	xmax = str(int(xmin)+int(width))
    	ymax = str(int(ymin)+int(height))
    	out_line = class_name+" 0.00 0.00 0.00 "+xmin+" "+ymin+" "+xmax+" "+ymax+" 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n"	
	    with open(out_file, "a") as o:
			o.write(out_line)