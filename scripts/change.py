from os import listdir
from os.path import isfile, join
import fileinput

onlyfiles = [f for f in listdir("/home/gilles/Documents/memoire/repos/insect-thesis/annotate-to-KITTI/data/noctuidae/labels") if isfile(join("/home/gilles/Documents/memoire/repos/insect-thesis/annotate-to-KITTI/data/noctuidae/labels", f))]
print(onlyfiles)
i = 0
while i<len(onlyfiles):
    onlyfiles[i]="/home/gilles/Documents/memoire/repos/insect-thesis/annotate-to-KITTI/data/noctuidae/labels/"+onlyfiles[i]
    i+=1
with fileinput.input(files=onlyfiles,inplace=True) as f:
    for line in f:
        print(line.replace("person","noctuidae"),end='')