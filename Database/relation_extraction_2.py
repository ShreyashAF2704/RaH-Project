import json
with open('logictree_for_neo4j_updated.json','rb') as file:
    data = json.load(file)
    


relations = []
all_nodes = []
all_nodes_ = []

def restructure_node(v):
    ele = {}
    
    ele["type"] = v["type"]
    #ele["Name"] = v["name"]
    
    if ele["type"] == "SELECTION":
        ele["type"] = "Problem"
        if "prompt" in v.keys():
            ele["desc"] = v["prompt"]
            
    if ele["type"] == "MESSAGE":
        if "payloads" in v.keys():
            ele["name"] = v["payloads"][0]
            ele["type"] = "Possible_Problem"
            
    return ele

for k,v in data["nodes"].items():
    ele = {}
    ele["id"] = v["id"]
    ele["Type"] = v["type"]
    ele["Name"] = v["name"]
    if "prompt" in v.keys():
        ele["prompt"] = v["prompt"]
    if "connections" in v.keys():
        ele["connections"] = [e["id"] for e in v["connections"] if e["id"] !=""]
         
    if "payloads" in v.keys():
        if type(v['payloads'][0]) == "dict":
            ele["payloads"] = [e["text"] for e in v["payloads"]]
        else:
            ele["payloads"] = v["payloads"]
    #print(ele)
    all_nodes.append(ele)
    all_nodes_.append(restructure_node(v))
    
    
    #print("-----------------------------------")

    
    if v["type"] == "SELECTION" and len(v["connections"]) == 1:
        print(k,v["prompt"])
        [print(ele["text"],ele["value"]) for ele in v["payloads"]]
        print(v["connections"])
        
        x = ""
        for key,value in data["nodes"].items():
            if key == v["connections"][0]["id"]:
                print(value["payloads"])
                x = value["connections"][0]["id"]
        id2_arr = []
        rel2_arr = []        
        for key,value in data["nodes"].items():
            if key == x:
                print(value["connections"])
                id2_arr = [ele["id"] for ele in value["connections"]]
                rel2_arr = [ele["text"] for ele in value["payloads"]]
                print(rel2_arr)
                print(id2_arr)
        
        [relations.append([k,"possible_problem",ele["id"]]) for ele in v["connections"]]
        
        print("----------")
    

#[print(ele) for ele in all_nodes]

for ele in all_nodes:
    print(ele)
    data1 = []
    data2 = []
    if ele["Type"] == "SELECTION":
        for i in ele["payloads"]:
            data1.append(i["text"])
        for i in ele["connections"]:
            data2.append(i)
        if len(data1) == len(data2):
            for i in range(len(data)):
                relations.append([ele["id"],data1[i],data2[i]])
        #print(data)
        #print(data2)
        #print("------")


all_relations_node = []
for ele in relations:      
    node1 = restructure_node(data["nodes"][str(ele[0])])
    node2 = {}
    node2["type"] = ele[1]
    node2["relation"] = ele[1]
    node3 = restructure_node(data["nodes"][ele[2]])
    
  
    all_relations_node.append([node1,node2,node3])
    print(node1)
    print(node2)
    print(node3)
    print("-----------------")
    
    
    #print(ele)

for i in all_nodes_:
    print(i)

ans_data = {}
ans_data["nodes"] = all_nodes_
ans_data["relations"] = all_relations_node

with open("result_mindtree.json","w") as file:
    json.dump(ans_data,file)