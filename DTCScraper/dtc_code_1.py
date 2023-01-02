import os
import glob
from bs4 import BeautifulSoup,Comment
import urllib.request
import requests
import json
import re
import pandas as pd 


uri = "https://www.totalcardiagnostics.com/support/Knowledgebase/Article/View/21/0/genericmanufacturer-obd2-codes-and-their-meanings#:~:text=Diagnostic%20trouble%20codes%20%28or%20fault%20codes%29%20are%20obd2,the%20normal%2Faccepted%20range%20%28Eg%3A%20fuel%20mixture%20too%20rich%29."

webpage = urllib.request.urlopen(uri).read()
soup = BeautifulSoup(webpage,'html.parser')
all_codes_div = soup.find_all("div",id="showorhide")
list_codes = []
count = 0
for i in range(len(all_codes_div)):
    for ele in all_codes_div[i].find_all("li"):
        e = ele.text
        while "  " in e:
            e = e.replace("  ","").replace("\t\xa0\xa0\xa0\xa0\xa0"," ")
        
        arr = re.split(" ",e,maxsplit=1)
        if len(arr) == 2:
            e_dict = {}
            e_dict["code"] = arr[0]
            e_dict["desc"] = arr[1]
            list_codes.append(e_dict)
df = pd.DataFrame(list_codes)
df.to_csv('DTC_Codes_1.csv')
print("Done")  