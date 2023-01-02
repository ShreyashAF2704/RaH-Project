import os
import glob
from bs4 import BeautifulSoup,Comment
import urllib.request
import requests
import json
import re
import pandas as pd 


uri = "https://www.engine-codes.com/make/ford/"




hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
req = urllib.request.Request(uri, headers=hdr)
webpage = urllib.request.urlopen(req).read()
soup = BeautifulSoup(webpage,'html.parser')

codes_list_div = soup.find_all("li",class_="cont cc-white")
for ele in codes_list_div:
    print(ele)