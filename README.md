# insect-thesis
## GBIF PARSER
This script has been made to simply download and eventually convert images that are referenced in the csv folder.
Sample usage : 

```
python3 gbif-parser.py insect path-to-multimedia-file number-of-images
```
where insect is a name of the insect that is in the images, path-to-multimedia-file is the path to the multimedia txt file that has been downloaded inside the archive of GBIF.org and number-of-images is the desired number of images downloaded.
This script will output images inside the path annotate-to-KITTI/data/insect/images. They all have jpeg format.