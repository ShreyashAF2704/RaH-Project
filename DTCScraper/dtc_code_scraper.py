import os
import glob
from bs4 import BeautifulSoup,Comment
import urllib.request
import requests
import json
import re
import pandas as pd 

with open("DTC_Codes.txt") as f:
    data = f.readlines()
 
for i in range(len(data)):
    if "" in data[i]:
        data[i] = data[i].replace("","")

Data_ = "" 

data_ = []
for i in range(len(data)):
    if re.match("P[0-9][0-9]",data[i][0:3]):
        data[i] = "Q_X"+data[i]
        Data_ += data[i] 
    elif data[i][0:4] == "Poss":
        data[i] = "_Poss"+data[i][4::]
        Data_ += data[i]
    else:
        Data_ += data[i]



ele_ = Data_.split("Q_X")[1::]

for ele in ele_:
    code_name = ele.split("Description:")[0]
    description = ele.split("Description:")[1].split("_Possible")[0]
    possible_cause = ele.split("Description:")[1].split("_Possible")[1].split("Diagnostic")[0]
    Diagnostic = ele.split("Description:")[1].split("_Possible")[1].split("Diagnostic")[1].split("Application")[0]

    
    dtc_dict = {}
    dtc_dict["code"] = code_name.split("-")[0]
    dtc_dict["topic"] = code_name.split("-")[1]
    dtc_dict["description"] = description.replace("\n","").replace("    ","")
    causes = []
    for cc_i in possible_cause.replace("\n","").replace("Causes:","").replace("☺","").split(""):
        ele = cc_i 
        while "  " in ele:
            ele = ele.replace("  ","")
        if ele != "" and ele != " ":
            causes.append(ele)
    
    dtc_dict["possible_cause"] = causes
    dtc_dict["Diagnostic"] = Diagnostic.replace("\n","").replace("Aids:","")
    diag = dtc_dict["Diagnostic"]
    while "  " in diag:
        diag = diag.replace("  ","")
    dtc_dict["Diagnostic"] = diag
    
    data_.append(dtc_dict)
    
    for x,y in dtc_dict.items():
        print(x)
        print(y)
        print("-")
    print("--------------")
    
    
df = pd.DataFrame(data_)
df.to_csv('DTC_Codes.csv')
