import os
import glob
from bs4 import BeautifulSoup,Comment
import urllib.request
import requests
import json

uri = "https://www.carproblemzoo.com/"
webpage = urllib.request.urlopen(uri).read()
#req = requests.get(uri)
soup = BeautifulSoup(webpage,'html.parser')
data_dir = os.getcwd()
data_dir = os.path.join(data_dir,"HondaData")


car_list_div = soup.find_all("span",class_="a-list")
cars_dict = {}
ans = []
cars_list = ["Honda"]


for i in range(len(car_list_div)):
    href = car_list_div[i].find("a")["href"]
    name = car_list_div[i].find("a").text
    if name in cars_list:
        cars_dict[name] = href 
print(cars_dict)
for cars in list(cars_dict.keys()):
    new_uri1 = uri+cars_dict[cars]
    page1 = urllib.request.urlopen(new_uri1).read()
    soup1 = BeautifulSoup(page1,'html.parser')
    
    model_list_div = soup1.find("table",class_="table table-condensed").find_all("td")
    model_dict = {}
    
    for i in range(len(model_list_div)):
        ele = model_list_div[i].find("a")
        if ele is not None:
            model_dict[ele.text] = ele["href"]
    
    m = ["Pilot"]
    for model in m:
        new_uri2 = "https://www.carproblemzoo.com"+model_dict[model]
        page2 = urllib.request.urlopen(new_uri2).read()
        soup2 = BeautifulSoup(page2,'html.parser')
        
        model_year_div = soup2.find("table",id="table1").find_all("td")
        model_year_dict = {}
        
        for i in range(len(model_year_div)):
            ele = model_year_div[i].find("a")
            if ele is not None:
                model_year_dict[ele.text] = ele["href"]
        
        y_arr = list(model_year_dict.keys())
        for year in y_arr:
            new_uri3 = new_uri2+model_year_dict[year]
            print(new_uri3)
            page3 = urllib.request.urlopen(new_uri3).read()
            soup3 = BeautifulSoup(page3,'html.parser')
            
            problem_list_div = soup3.find("table",class_="table table-condensed").find_all("td")
            problem_dict = {}
            
            for i in range(len(problem_list_div)):
                ele = problem_list_div[i].find("a")
                if ele is not None:
                    problem_dict[ele.text] = ele["href"]
            
            for problem in problem_dict.keys():
                new_uri4 = new_uri3+problem_dict[problem]
                print(new_uri4)
                page4 = urllib.request.urlopen(new_uri4).read()
                soup4 = BeautifulSoup(page4,'html.parser')
                
                sub_problem_list_div = soup4.find("table",class_="table table-condensed").find_all("td")
                sub_problem_dict = {}
                
                for i in range(len(sub_problem_list_div)):
                    ele = sub_problem_list_div[i].find("a")
                    if ele is not None:
                        sub_problem_dict[ele.text] = ele["href"]    
                
                for sub_problem in sub_problem_dict.keys():
                    new_uri5 = new_uri3+sub_problem_dict[sub_problem]
                    page5 = urllib.request.urlopen(new_uri5).read()
                    soup5 = BeautifulSoup(page5,'html.parser')
                    
                    problem_desc_div = soup5.find_all("div",class_="problem-item")
                    
                  
                    
                    for i_subp in range(len(problem_desc_div)):
                        if problem_desc_div[i_subp].find("div",class_="faildate-float") == None:
                            failure_date = "None"
                        else:
                            failure_date = problem_desc_div[i_subp].find("div",class_="faildate-float").text
                        description = problem_desc_div[i_subp].find("p",class_="ptext_list").text
                        description = description.replace("\r\n","")
                        
                        failure_date = failure_date.replace("\r\n","").replace("\n","")
                        problem_desc_dict = {}
                        problem_desc_dict["Vehicle"] = cars
                        problem_desc_dict["Model"] = model
                        problem_desc_dict["Model Year"] = year.replace("\r\n","")
                        problem_desc_dict["Problem"] = problem
                        problem_desc_dict["Sub Problem"] = sub_problem
                        problem_desc_dict["description"] = description.replace("\r\n","")
                        problem_desc_dict["fail date"] = failure_date.replace("Failure Date:","")
                        #print(problem_desc_dict)
                        ans.append(problem_desc_dict)
                    
                    
                    name = "Honda__"+str(model)+"_"+str(year.replace("\r\n",""))+".json"
                    file = os.path.join(data_dir,name)
                    with open(file, "w") as final:
                        json.dump(ans, final)
                        print("Data Saved")
                    break
                    
                    
                
            ans = []
    