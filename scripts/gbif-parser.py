import urllib.request
import sys
import time
import tqdm
from multiprocessing import Pool
import multiprocessing.pool as mpp

from os import path, remove

from os.path import isfile, join, exists

from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool

import os

# istarmap.py for Python 3.8+
import multiprocessing.pool as mpp

#source for loading bar : https://stackoverflow.com/questions/57354700/starmap-combined-with-tqdm
def istarmap(self, func, iterable, chunksize=1):
    """starmap-version of imap
    """
    self._check_running()
    if chunksize < 1:
        raise ValueError(
            "Chunksize must be 1+, not {0:n}".format(
                chunksize))

    task_batches = mpp.Pool._get_tasks(func, iterable, chunksize)
    result = mpp.IMapIterator(self)
    self._taskqueue.put(
        (
            self._guarded_task_generation(result._job,
                                          mpp.starmapstar,
                                          task_batches),
            result._set_length
        ))
    return (item for chunk in result for item in chunk)


mpp.Pool.istarmap = istarmap

def get_url(element,counter,name,sizex,sizey):
    try:
        if element[0] == "image/jpeg":
            #print("saving to","data/kitti/"+name+"/inference/"+str(counter)+"-"+name+".jpg")
            urllib.request.urlretrieve(element[1], "../data/kitti/"+name+"/inference/images/"+str(counter)+"-"+name+".jpg")
            if sizex!=0 and sizey!=0:
                image = Image.open("../data/kitti/"+name+"/inference/images/"+str(counter)+"-"+name+".jpg")
                new_image = image.resize((sizex,sizey))
                new_image.save("../data/kitti/"+name+"/inference/images/"+str(counter)+"-"+name+".jpg")
        elif element[0] == "image/png":
            urllib.request.urlretrieve(element[1], "../data/kitti/"+name+"/inference/images/"+str(counter)+"-"+name+".png")
            im = Image.open("../data/kitti/"+name+"/inference/images/"+str(counter)+"-"+name+".png")
            if not im.mode == 'RGB':
                im = im.convert('RGB')
            if sizex!=0 and sizey!=0:
                im = im.resize((sizex,sizey))
            im.save("../data/kitti/"+name+"/inference/images/"+str(counter)+"-"+name+".jpg", quality=100)
            os.remove("../data/kitti"+name+"/inference/images/"+str(counter)+"-"+name+".png")
    except:
        pass


if __name__=='__main__':  
    print("First argument : name of the species")
    print("Second argument : txt file containing links in gbif multimedia format")
    print("Third argument : number of images to download")
    print("Fourth argument : size width for the image to be resized")
    print("Fifth argument : size height for the image to be resized")
    print("INFO : Images will be downloaded directly into inference folder of the dataset, since nothing is annotated")
    name = sys.argv[1]

    f = open(sys.argv[2],"r")
    sizex=0
    sizey=0
    

    # number of files to be downloaded
    target_number = int(sys.argv[3])
    
    if len(sys.argv)>4:
        sizex = int(sys.argv[4])
        sizey = int(sys.argv[5])
    firstline=True
    targets = []
    # creation of folders
    if not path.exists("../data") : os.mkdir("../data")
    if not path.exists("../data/kitti") : os.mkdir("../data/kitti")
    if not path.exists("../data/kitti/"+name) : os.mkdir("../data/kitti/"+name)
    if not path.exists("../data/kitti/"+name+"/inference") : os.mkdir("../data/kitti/"+name+"/inference")
    if not path.exists("../data/kitti/"+name+"/train") : os.mkdir("../data/kitti/"+name+"/train")
    if not path.exists("../data/kitti/"+name+"/train/images") : os.mkdir("../data/kitti/"+name+"/train/images")
    if not path.exists("../data/kitti/"+name+"/inference/images") : os.mkdir("../data/kitti/"+name+"/inference/images")

    if not path.exists("../data/kitti/"+name+"/train/labels") : os.mkdir("../data/kitti/"+name+"/train/labels")
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
    listsizex = [sizex for i in range(0,len(targets))]
    listsizey = [sizey for i in range(0,len(targets))]
    #pool = ThreadPool(100)
    inputs = zip(targets, counter_list, names,listsizex,listsizey)
    with mpp.Pool(2) as pool:
        results = list(tqdm.tqdm(pool.istarmap(get_url,inputs),total=len(targets)))

    print(str(len(targets)),"files successfully saved in path ","data/kitti/"+name+"/inference/images/*")
