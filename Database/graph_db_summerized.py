from neo4j import GraphDatabase

URI = "bolt://localhost:7687/"
AUTH = ("shreyash", "1234")
driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session(database="demo2")

#----------universal read---------- 
#get all cars
def get_car_data(tx):
    result = tx.run("""
             MATCH (n:Car) return n
             """)
    record = list(result)
    return record

   
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

#Fetch all cars or Logic Trees		
def fetch_cars():
    r = session.execute_read(get_car_data)
    cars = [ele.data()["n"] for ele in r]
    return cars
    
    
def fetch_relation_for_node():
    data = {}
    data["type"] = "Problem"
    data["desc"] = 'Did you attempt to jump start the car or charge the battery?'
    rel = session.execute_read(get_relations,data)
    #print(rel)
    ans = []
    for i in rel:
        ans.append([ i.data()["r"][1] , i.data()["r"][2] ])
    for i in ans:
        print(i)
    #print(ans)
fetch_relation_for_node()