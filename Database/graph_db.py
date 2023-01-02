from neo4j import GraphDatabase


URI = "bolt://localhost:7687/"
AUTH = ("shreyash", "1234")


#--get request---------------
def get_all(tx):
    result = tx.run("""
           MATCH n=()-[r]->() return n
           """)
    record = list(result)
    return record

def get_specific_node(tx,node,data,parameter):
    result =tx.run("Match (n:"+str(node)+") WHERE n."+str(parameter)+"=$data return n",data=data)
    record = list(result)
    return record
        
def get_car_data(tx):
    result = tx.run("""
             MATCH (n:Car) return n
             """)
    record = list(result)
    return record

def get_relation_for_car(tx,name):
    result = tx.run("""
             Match (n:Car{Name:$name})-[r]->() return r
             """,name=name)
    record = list(result)
    return record


def get_NextNode_from_relation(tx,relation):
    query = "MATCH (n)-[r:"+str(relation)+"]->(m) return m"
    result = tx.run(query)
    record = list(result)
    return record


def get_NextRelation_from_node(tx,name):
    result = tx.run("""
             MATCH (n:Problem{name:$name})-[r]->() return r
             """,name=name)
    record = list(result)
    return record

#----------universal read----------    
#get relation's from node
def get_relations(tx,data):
    type_node = data["type"]
    if type_node == "Car":
        Name = data["Name"]
        #Id = data["Id"]
        result = tx.run("Match (n:Car) where n.Name=$Name Match p=(n)-[r]->(m) return r,m",Name=Name)
        return list(result)
        
    elif type_node == "Problem":
        desc = data["desc"]
        #Id = data["Id"]
        result = tx.run("Match (n:Problem) Where n.desc=$desc Match (n)-[r]->(m) return r,m",desc=desc)
        return list(result)
        
    elif type_node == "Possible_Problem":
        Name = data["Name"]
        #Id = data["Id"]
        result = tx.run()
        return list(result)
    else:
        return "No Such Node Exist"

#get node and its relation from prev node and relation
def get_next_node_relation(tx,node,relation):
    type_node = data["type"]
    if type_node == "Car":
        Name = data["Name"]
        #Id = data["Id"]
        Relation = relation["name"]
        result = tx.run("Match ")
        return result
        
    elif type_node == "Problem":
        desc = data["desc"]
        Id = data["Id"]
        Relation = relation["name"]
        result = tx.run()
        return result
        
    elif type_node == "Possible_Problem":
        Name = data["Name"]
        Id = data["Id"]
        Relation = relation["name"]
        result = tx.run()
        return result
    else:
        return "No Such Node Exist"
#-----------------------------------
#-----------Write operation--------

def add_car(tx,data):
    result = tx.run("Create (a:Car) "
                    "SET a.Name = $name "
                    "SET a.Year = $year "
                    "SET a.model = $model "
                    "RETURN a.Name +', from node '+id(a)",
                    name=data[0],model=data[1],year=data[2]
                    )
    return result.single()[0]
           
def add_Car_Problem_relationship(tx,data):
    car = data[0]
    problem = data[1]
    relation = data[2]
    result = tx.run("Create (n:Car) Create(m:Problem) "
                    "SET n.Name=$name "
                    "SET n.Model=$model "
                    "SET n.Year=$year "
                    "SET m.desc=$desc "
                    "Create (n)-[r:"+str(relation)+"]->(m) "
                    "RETURN 'Done. New Relation is created between nodes.' ",
                    name=car[0],model=car[1],year=car[2],desc=problem
                    )
    return result.single()[0]
    
    
    
    
    
def add_nodes(tx,node):
    print(node)
    if node["type"] == "Car":
        result = tx.run("Create (n:Car) SET n.Name=$name SET n.Model = $model SET n.Year = $year Return n.Name +' Created.' ",name=node["Name"],model=node["Model"],year=node["Year"])
        return result.single()[0]
    elif node["type"] == "Possible_Problem":
        result = tx.run("Create (n:Possible_Problem) set n.name=$name return n.name +'Created'",name=node["name"])
        return result.single()[0]
    else:
        result = tx.run("Create (n:Problem) set n.desc=$desc return n.desc +' Created'",desc=node["desc"])
        return result.single()[0]
        
def add_relationship(tx,data):
    print(data)
    node1 = data[0]
    node2 = data[1]
    node3 = data[2]
    numbers = ["Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine"]
    relation = node2["name"] 
    #.replace(" ","_").replace("-","_")
    
    '''
    if "-" in node2["relation"]:
        rel = node2["relation"].split('-')
        relation = ""
        for r in rel:
            relation += "year_"+str(r)+"_"
    if relation.isnumeric():
            relation = "year_"+str(relation)
    '''
    
    if node1["type"] == "Car" and node3["type"] == "desc":
        result = tx.run("Match (n:Car) where n.Name = $name Match (m:Problem) where m.desc = $desc Create (n)-[r:"+str(relation)+"]->(m) SET r.relation=$relation Return 'Relation Created'",name=node1["Name"],desc=node3["desc"],relation=relation)
        return result.single()[0]
         
    elif node1["type"] == "desc" and node3["type"] == "desc":
        result = tx.run("Match (n:Problem) where n.desc=$desc1 Match (m:Problem) where m.desc=$desc2 Create (n)-[r:"+str(relation)+"]->(m) SET r.relation=$relation Return 'Relation Created'",desc1=node1["desc"],desc2=node3["desc"],relation=relation) 
        return result.single()[0]
    else:
        result = tx.run("Match (n:Problem) where n.desc=$desc Match (m:Possible_Problem) where m.name=$name Create (n)-[r:"+str(relation)+"]->(m) SET r.relation=$relation Return 'Relation Created'",desc=node1["desc"],name=node3["name"],relation=relation) 
        return result.single()[0]

    
    
driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session(database="demo2")

#--------------------------------------------------------------------
def get_all_data():
    data = session.execute_read(get_all)
    
    for i in data:
        print(i.data())

#get all cars
def get_cars():
    r = session.execute_read(get_car_data)
    for i in r:
        print(i.data())
    cars = [ele.data()["n"] for ele in r]
    return cars

#get all relation for a car       
def get_relation_car(car_name):
    car_r = session.execute_read(get_relation_for_car,name=car_name)
    relations = [ele.data()['r'][1] for ele in car_r]
    return relations

def get_problem_from_Problem_relation(relation):
    rel = session.execute_read(get_NextNode_from_relation,relation=relation)
    #nodes = [ele.data()["m"]["name"] for ele in rel]
    desc  = [ele.data()["m"]["desc"] for ele in rel]
    return desc
def get_relation_from_problem(problem):
    rel = session.execute_read(get_NextRelation_from_node,name=problem)
    relation = [ele.data()["r"][1] for ele in rel]
    print(relation)


def fetch_relation_for_node():
    data = {}
    data["type"] = "Problem"
    data["desc"] = 'Does it turn Over?'
    rel = session.execute_read(get_relations,data)
    ans = []
    for i in rel:
        ans.append([ i.data()["r"][1] , i.data()["r"][2] ])
    for i in ans:
        print(i)
    #print(ans)
#--------------------------------------------------------------------

def create_car(data):
    res = session.execute_write(add_car,data)
    print(res)

def create_car_problem(data):
    res = session.execute_write(add_Car_Problem_relationship,data)
    print(res)

def Check_If_Node_exist(node,data):
    if node == "Car":
        res = session.execute_read(get_specific_node,node=node,data=data,parameter="Name")
    if node == "Problem":
        res = session.execute_read(get_specific_node,node,data,parameter="desc")
    if node == "Possible_Problem":
        res = session.execute_read(get_specific_node,node,data,parameter="Name")

    data= [ele.data() for ele in res]
    print(data)
    return len(data)>0
    
def CreateNodes(data):
    for i in range(len(data)):
        res = session.execute_write(add_nodes,data[i])
        print(res)


def Add_bulk_data(data):
    for i in range(0,len(data)):
        rel = session.execute_write(add_relationship,data[i])
        print(i," ",rel) 
    
        


#--------------------------------------------------------------------------------------------
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


        
    

#CreateNodes(nodes)
#Add_bulk_data(arr)
fetch_relation_for_node()

'''
new_data = {}
with open('result_mindtree.json','r') as file:
    new_data = json.load(file)
    CreateNodes(new_data["nodes"])
    Add_bulk_data(new_data["relations"])
'''
#create_car_problem([["Toyota","Fortuner","2003"],"Brakes failed while driving","Brakes_Issue"])















