import pandas as pd
import json
import os

curdir = os.getcwd()
data_dir = os.path.join(curdir,"Ford Explorer")
files = os.listdir(data_dir)
print(files)
data = []
for i in range(len(files)):
    filename = os.path.join(data_dir,files[i])
    print(filename)
    with open(filename,"r") as f:
        ele = json.load(f)
        for j in range(len(ele)):
            description = ele[j]["description"]
            description = description.replace("\n","")
            description = description.replace("A D V E R T I S E M E N T S","")
            ele[j]["description"] = description
            
            

        print(len(data),len(ele))
        data = data+ele
        print("Combined Data :",len(data))


    
df = pd.DataFrame(data)
df.to_csv('Ford_Explorer.csv')
