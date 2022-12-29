import os
import glob
from bs4 import BeautifulSoup,Comment
import urllib.request
import requests
import json

uri = "https://www.carcomplaints.com/"
webpage = urllib.request.urlopen(uri).read()
#req = requests.get(uri)
soup = BeautifulSoup(webpage,'html.parser')
print(soup)
section = soup.section.find_all('a')

data_dir = os.getcwd()
data_dir = os.path.join(data_dir,"Ford Explorer")

ans = []
count_data = 0

#list of all cars
car_dict = {}
cars = []



for i in section:
    car_dict[i.text] = i["href"]
    cars.append(i.text)
print("level1 completed")
print(cars)

for i in range(8,9):
    new_uri = uri+cars[i]
    print(new_uri)
    page = urllib.request.urlopen(new_uri).read()
    soup2 = BeautifulSoup(page,'html.parser')
    
    models_div = soup2.div.find_all("ul",class_="column bar")
    model = []
    model_dict = {}

    
    #get list of all models
    for j in range(len(models_div)):
        for li in models_div[j].find_all("a"):
            print(li.text,"=>",li["href"])
            model.append(li.text)
            model_dict[li.text] = li["href"]
    print(model_dict)

    '''
    model = ["Explorer"]
    model_dict = {}
    model_dict["Explorer"] = "Ford/Explorer/"
    
    '''
    print("level2 completed")

    
   
    for models in model:
        new_uri2 = uri+model_dict[models]
        print(new_uri2)
        page2 = urllib.request.urlopen(new_uri2).read()
        soup3 = BeautifulSoup(page2,'html.parser')

        model_year = []
        model_year_div = soup3.div.find("ul",class_="timeline")

        count_p = []
        
        #list of model year
        for li_year in model_year_div.find_all("span",class_="label"):
            print(li_year.text)
            model_year.append(li_year.text)

        for c in model_year_div.find_all("span",class_="count"):
            print(c.text)
            count_p.append(c.text)
        
        new_model_year = []
        
        for count_ele in range(len(model_year)):
            co = count_p[count_ele].replace(",","")
            if int(co) != 0:
                new_model_year.append(model_year[count_ele])
        print(new_model_year)
        print("level3 completed")

        
        for year in new_model_year:
            new_uri3 = new_uri2+year+"/"
            print(new_uri3)
            page3 = urllib.request.urlopen(new_uri3).read()
            soup4 = BeautifulSoup(page3,'html.parser')
            problem_div = soup4.find("div",id="graph").find_all("li")
            problem_dict = {}

            
            #list of problems
            for li_problem in range(len(problem_div)):
                a_tag = problem_div[li_problem].find("a")
                strong = problem_div[li_problem].find("strong")
                print(a_tag["href"],"=>",strong.text)
                problem_dict[strong.text] = a_tag["href"]

            print("level4 completed")
            prob_arr = list(problem_dict.keys())
            
            for prob in prob_arr:
                print(problem_dict[prob])
                new_uri4 = new_uri3+problem_dict[prob]
                print(new_uri4)
                page4 = urllib.request.urlopen(new_uri4).read()
                soup5 = BeautifulSoup(page4,'html.parser')

                sub_problems = soup5.find("div",id="graph").find_all("li")
                sub_problem_dict = {}
                #list of sub problems
                for li_subproblem in range(len(sub_problems)):
                    a_tag_sub = sub_problems[li_subproblem].find("a")
                    strong_sub = sub_problems[li_subproblem].find("strong")
                    print(a_tag_sub["href"],"=>",strong_sub.text)
                    sub_problem_dict[strong_sub.text] = a_tag_sub["href"]
                print("level5 completed")
                for sub_prob in list(sub_problem_dict.keys()):
                    new_uri5 = "https://www.carcomplaints.com"+sub_problem_dict[sub_prob]
                    print(new_uri5,"------------")
                    page5 = urllib.request.urlopen(new_uri5).read()
                    soup6 = BeautifulSoup(page5,'html.parser')
        
                    problem_desc_dict = {}
                    
                    problem_desc_div = soup6.find_all("div",class_="complaint")
                    #print(problem_desc_div)
                    for ele in range(len(problem_desc_div)):
                        title = problem_desc_div[ele].find("h3",class_="ptitle").text
                        problem_distance = problem_desc_div[ele].find("div",class_="cheader").find_all("li")

                        if len(problem_distance) == 1:
                            if "miles" in problem_distance[0]:
                                distance = problem_distance[0].text
                                problem = ""
                            else:
                                problem = problem_distance[0].text
                                distance = ""
                        else:
                            problem = problem_distance[0].text
                            distance = problem_distance[1].text
                            
                        problem_distance = [ele.text for ele in problem_distance]
                        description = problem_desc_div[ele].find("div",class_="comments").text
                        description = description.replace("\n","")
                        description = description.replace("A D V E R T I S E M E N T S","")

                        ans_new = {}
                        ans_new["Vehicle"] = cars[i]
                        ans_new["Model"] = models
                        ans_new["Model Year"] = year
                        ans_new["Problem"] = prob
                        ans_new["Sub Problem"] = sub_prob
                        ans_new["Model Title"] = title
                        ans_new["Model Problem"] = problem
                        ans_new["distance covered"] = distance
                        ans_new["description"] = description

                        ans.append(ans_new)
                        #print(ans_new)
                        
                        print("--------------------------------------------------------------")
                        
                    name = "Ford__new_"+str(models)+"_"+str(year)+".json"
                    file = os.path.join(data_dir,name)
                    with open(file, "w") as final:
                        json.dump(ans, final)
                        print("Data Saved")
                        
            ans = []

    

