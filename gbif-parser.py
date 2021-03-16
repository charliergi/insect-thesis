import urllib.request
import sys
from os import path, remove
from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool

import os

def get_url(element,counter,name):
    try:
        if element[0] == "image/jpeg":
            print("saving to","annotate-to-KITTI/data/"+name+"/images/"+str(counter)+".jpg")
            urllib.request.urlretrieve(element[1], "annotate-to-KITTI/data/"+name+"/images/"+str(counter)+".jpg")
        elif element[0] == "image/png":
            urllib.request.urlretrieve(element[1], "annotate-to-KITTI/data/"+name+"/images/"+str(counter)+".png")
            im = Image.open("annotate-to-KITTI/data/"+name+"/"+str(counter)+".png")
            if not im.mode == 'RGB':
                im = im.convert('RGB')
            im.save("annotate-to-KITTI/data/"+name+"/images/"+str(counter)+".jpg", quality=95)
            os.remove("annotate-to-KITTI/data/"+name+"/"+str(counter)+".png")
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
    if not path.exists("annotate-to-KITTI/data/"+name) : os.mkdir("annotate-to-KITTI/data/"+name)
    if not path.exists("annotate-to-KITTI/data/"+name+"/images") : os.mkdir("annotate-to-KITTI/data/"+name+"/images")
    for i in f.readlines():
        print(i)
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
    print(results)

    print(str(len(targets)),"files successfully saved !")
