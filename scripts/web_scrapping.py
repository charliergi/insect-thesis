import requests
import os
import urllib.request
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("species_number", help="the number corresponding to the species on observation.be")
args = parser.parse_args()

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def make_url(species, page):
	url = 'https://observations.be/species/'+str(species)+'/photos/?after_date=1991-03-07&before_date=2021-02-27&advanced=on&is_validated=on&life_stage=IMAGO&page='+str(page)
	return url

page_number = 1
species_number = args.species_number
url = make_url(species_number, page_number)

result = requests.get(url).text
soup = bs(result, 'lxml')

#create a folder with the same name as the species
species_name = soup.find('span', {'class' : 'species-common-name'}).get_text()
cwd = os.getcwd()
out_folder = os.path.join(cwd,species_name)
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

#downloads every image of that species
downloaded_images = 0
while is_valid(url) and downloaded_images <= 1000:
	result = requests.get(url).text
	soup = bs(result, 'lxml')
	for img_tag in soup.select('a.lightbox-gallery-image'):
		img = img_tag.attrs.get('href')
		img_name = str(img.split('/')[-1])
		print(img_name)
		img = 'https://observations.be'+img
		urllib.request.urlretrieve(img, os.path.join(out_folder, img_name))
		downloaded_images+=1
	page_number+=1
	url = make_url(species_number,page_number)
