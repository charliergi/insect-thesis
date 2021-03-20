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

def get_url(element,counter,name):
    try:
        if element[0] == "image/jpeg":
            #print("saving to","data/kitti/"+name+"/test/"+str(counter)+"-"+name+".jpg")
            urllib.request.urlretrieve(element[1], "data/kitti/"+name+"/test/images/"+str(counter)+"-"+name+".jpg")
        elif element[0] == "image/png":
            urllib.request.urlretrieve(element[1], "data/kitti/"+name+"/test/images/"+str(counter)+"-"+name+".png")
            im = Image.open("data/kitti/"+name+"/test/images/"+str(counter)+"-"+name+".png")
            if not im.mode == 'RGB':
                im = im.convert('RGB')
            im.save("data/kitti/"+name+"/test/images/"+str(counter)+"-"+name+".jpg", quality=100)
            os.remove("data/kitti"+name+"/test/images/"+str(counter)+"-"+name+".png")
    except:
        pass


if __name__=='__main__':  
    print("First argument : name of the species")
    print("Second argument : txt file containing links in gbif multimedia format")
    print("Third argument : number of iamges to download")
    print("INFO : Images will be downloaded directly into test folder of the dataset, since nothing is annotated")
    name = sys.argv[1]

    f = open(sys.argv[2],"r")

    # number of files to be downloaded
    target_number = int(sys.argv[3])
    firstline=True
    targets = []
    # creation of folders
    if not path.exists("data") : os.mkdir("data")
    if not path.exists("data/kitti") : os.mkdir("data/kitti")
    if not path.exists("data/kitti/"+name) : os.mkdir("data/kitti/"+name)
    if not path.exists("data/kitti/"+name+"/test") : os.mkdir("data/kitti/"+name+"/test")
    if not path.exists("data/kitti/"+name+"/train") : os.mkdir("data/kitti/"+name+"/train")
    if not path.exists("data/kitti/"+name+"/train/images") : os.mkdir("data/kitti/"+name+"/train/images")
    if not path.exists("data/kitti/"+name+"/test/images") : os.mkdir("data/kitti/"+name+"/test/images")

    if not path.exists("data/kitti/"+name+"/train/labels") : os.mkdir("data/kitti/"+name+"/train/labels")
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
    #pool = ThreadPool(100)
    inputs = zip(targets, counter_list, names)
    with mpp.Pool(12) as pool:
        results = list(tqdm.tqdm(pool.istarmap(get_url,inputs),total=len(targets)))

    print(str(len(targets)),"files successfully saved in path ","data/kitti/"+name+"/test/*")
