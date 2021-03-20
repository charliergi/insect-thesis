import urllib.request
import sys
import time
from os import path, remove

from os.path import isfile, join, exists

from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool

import os



def get_url(element,counter,name):
    try:
        if element[0] == "image/jpeg":
            print("saving to","data/"+name+"/images/"+str(counter)+"-"+name+".jpg")
            urllib.request.urlretrieve(element[1], "data/"+name+"/images/"+str(counter)+"-"+name+".jpg")
        elif element[0] == "image/png":
            urllib.request.urlretrieve(element[1], "data/"+name+"/images/"+str(counter)+"-"+name+".png")
            im = Image.open("data/"+name+"/"+str(counter)+"-"+name+".png")
            if not im.mode == 'RGB':
                im = im.convert('RGB')
            im.save("data/"+name+"/images/"+str(counter)+"-"+name+".jpg", quality=95)
            os.remove("data/"+name+"/"+str(counter)+"-"+name+".png")
    except:
        pass


if __name__=='__main__':  
    print("please insert as first parameter the name of the folder where you want to put the data, and on second the name of the multimedia.csv")
    print("third argument specifies number of files to be downloaded")
    name = sys.argv[1]

    f = open(sys.argv[2],"r")

    # number of files to be downloaded
    target_number = int(sys.argv[3])
    firstline=True
    targets = []
    if not path.exists("data/"+name) : os.mkdir("data/"+name)
    if not path.exists("data/"+name+"/images") : os.mkdir("data/"+name+"/images")
    for i in f.readlines():
        if firstline:
            firstline=False
        else:
            s = i.split("\t")
            file_format = s[2]
            url = s[3]
            targets.append((file_format,url))
        if len(targets)==target_number:
            break
    f.close()
    counter_list=[i for i in range(0,len(targets))]
    names = [name for i in range(0,len(targets))]
    pool = ThreadPool(100)
    results = pool.starmap(get_url, zip(targets, counter_list, names))

    print(str(len(targets)),"files successfully saved in path ","data/"+name+"/images/*")
