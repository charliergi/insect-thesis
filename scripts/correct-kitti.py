import sys
import os
from os import listdir, path
from os.path import isfile, join
import fileinput

# on veut que toutes les images qui n'ont pas de labels bougent dans test/images
dataset_path = sys.argv[1]
dataset_labels_path = dataset_path + "/train/labels"



dataset_labels = [f for f in listdir(dataset_labels_path) if isfile(join(dataset_labels_path, f))]

for file in dataset_labels:
    new_file_content = ""
    with open(dataset_labels_path+"/"+file,"r") as reading_file:
        for line in reading_file.readlines():
            stripped_line = line.strip()
            if len(stripped_line.split(" "))>15:
                corrected_array = stripped_line.split(" ")[:15-len(stripped_line.split(" "))]
                corrected_line = ' '.join([str(elem) for elem in corrected_array])
                new_line = stripped_line.replace(stripped_line,corrected_line)
                new_file_content += new_line +"\n"
            else:
                new_file_content+=line
    
    with open(dataset_labels_path+"/"+file,"w") as writing_file:
        if(new_file_content!=""):
            writing_file.write(new_file_content)
    

    