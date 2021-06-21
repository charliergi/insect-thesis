# Scripts

[KITTI_to_YOLO.py](KITTI_to_YOLO.py) transforms a label file from the kitti data format to the yolo data format

[anchors.py](anchors.py) plots a representation of anchors as used by faster-rcnn

[capture-jetson.py](capture-jetson.py) a script usasble by a Jetson Nano to capture pictures from a cammera feed whenever it detects movement

[capture-test.py](capture-test.py) a script usasble by any compuer with a webcam to capture pictures from the feed whenever it detects movement

[change.py](change.py) replace a string present in file names by another string

[correct-kitti.py](correct-kitti.py) parse label files and remove errors

[csv_to_KITTI.py](csv_to_KITTI.py) transforms the labels present in a csv to the kitti data format in separate files for each corresponding image

[detection_generator.py](detection_generator.py) generates data to represent what our automated trap's logs can look like

[gbif-parser.py](gbif-parser.py) parse the links given by gbif in a file to download the dataset

[jpg_to_png.py](jpg_to_png.py) converts images from jpg to png

[mosaic_augmentation.py](mosaic_augmentation.py) generates mosaics of multiple images with semi-randomised positions

[organize.py](organize.py) creates the folder structure to be used in our annotation process

[transfer.py](transfer.py) all the unnatotated images are moved to another folder

[visualize_2D_kitti_annotations.py](visualize_2D_kitti_annotations.py) outputs images where the inference results are drawn, to visualise annotations

[web_scrapping.py](web_scrapping.py) web scrapping to download images of a species of insect on observation.be
