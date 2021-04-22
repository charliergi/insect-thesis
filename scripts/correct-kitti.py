import sys
import os
from os import listdir, path, stat
from os.path import isfile, join
import fileinput

LABELS = ["noctuidae","geometridae","hemiptera","hymenoptera","orthoptera","diptera","coleoptera","odonata","trichoptera"]
dataset_path = sys.argv[1]
dataset_labels_path = dataset_path + "/train/labels/"
dataset_images_path = dataset_path + "/train/images/"

# input : a KITTI line produced by inference or not.
# output : a corrected KITTI line with prediction confidence removed. --> 15 lines max
def correct_predictions(line):
    if len(line.split(" "))>15:
        corrected_array = line.split(" ")[:15-len(line.split(" "))]
        corrected_line = ' '.join([str(elem) for elem in corrected_array])
        return corrected_line
    return line

# indicates to the user that the line contains an incorrect label name
def correct_label_name(filename,line):
    if line.split(" ")[0] not in LABELS:
        print("invalid label !! ",line.split(" ")[0],line.split(" ")[0]+" in "+filename, "please correct it!")
        return -1
    return 0

# indicates to the user that 
def correct_rectangle(filename,line):
    xmin=int(float(line.split(" ")[4]))
    ymin=int(float(line.split(" ")[5]))
    xmax=int(float(line.split(" ")[6]))
    ymax=int(float(line.split(" ")[7]))
    if abs(xmax-xmin)<10 or abs(ymax-ymin)<10:
        print("incorrect rectangle for "+filename, "removing this line")
        return ""
    else:
        return line

dataset_labels = [f for f in listdir(dataset_labels_path) if isfile(join(dataset_labels_path, f))]
dataset_images = [f for f in listdir(dataset_images_path) if isfile(join(dataset_images_path, f))]

for file in dataset_labels:
    if os.stat(dataset_labels_path+file).st_size==0:
        print("empty label file",file,"removing it as well as its image")
        os.remove(dataset_labels_path+file)
        os.remove(dataset_images_path+(file.split(".")[0])+".jpg")
        continue
    
    if file.split(".")[0]+".jpg" not in dataset_images:
        os.remove(dataset_labels_path+file)
        continue
    
    new_file_content = ""
    incorrect=False
    with open(dataset_labels_path+file,"r") as reading_file:
        for line in reading_file.readlines():
            stripped_line = line.strip()
            if correct_label_name(file,stripped_line)==0:
                new_line = correct_predictions(stripped_line)
                if correct_rectangle(file,new_line)=="":
                    continue
                new_file_content += new_line +"\n"
            else:
                incorrect=True

    # nothing is valid in this file, removing it
    if new_file_content=="" or incorrect:
        print("removing file",file,"because nothing valid")
        os.remove(dataset_labels_path+file)
        os.remove(dataset_images_path+(file.split(".")[0])+".jpg")
        continue
    
    with open(dataset_labels_path+file,"w") as writing_file:
        if(new_file_content!=""):
            writing_file.write(new_file_content)
    

    