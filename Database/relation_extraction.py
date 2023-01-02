import json
with open('records_1.json','rb') as file:
    data = json.load(file)
	
    
arr = []
c = 0
for key in data["nodes"]:
    ele = []
    ele.append(key["p"]["segments"][0]["start"]["properties"])
    ele.append(key["p"]["segments"][0]["relationship"]["properties"])
    ele.append(key["p"]["segments"][0]["end"]["properties"])
    arr.append(ele)
    

nodes = []
car = []
problem = []
pp = []

for i in range(len(arr)):

    if arr[i][0]["type"] == "Car" and arr[i][0]["Name"] not in car:
        nodes.append(arr[i][0])
        car.append(arr[i][0]["Name"])
        
    if arr[i][0]["type"] == "desc" and arr[i][0]["desc"] not in problem:
        nodes.append(arr[i][0])
        problem.append(arr[i][0]["desc"])
        
    if arr[i][0]["type"] == "Possible_Problem" and arr[i][0]["name"] not in pp:
        nodes.append(arr[i][0])
        pp.append(arr[i][0]["name"])
        
    if arr[i][2]["type"] == "Car"and arr[i][2]["Name"] not in car:
        nodes.append(arr[i][2])
        car.append(arr[i][2]["Name"])
        
    if arr[i][2]["type"] == "desc"and arr[i][2]["desc"] not in problem:
        nodes.append(arr[i][2])
        problem.append(arr[i][2]["desc"])
        
    if arr[i][2]["type"] == "Possible_Problem" and arr[i][2]["name"] not in pp:
        nodes.append(arr[i][2])
        pp.append(arr[i][2]["name"])
        
        
[print(ele) for ele in arr]
    