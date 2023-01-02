import os
import glob
from bs4 import BeautifulSoup,Comment
import urllib.request
import requests
import json

uri = "https://www.dtcdecode.com/Ford"
webpage = urllib.request.urlopen(uri).read()
soup = BeautifulSoup(webpage,'html.parser')

ans = []
all_codes_dict = []

all_codes_div = soup.find_all("fieldset")

