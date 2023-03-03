import json
import os
import pandas as pd
import csv
from neo4j import GraphDatabase

class Neo4jDB:
    URI = ""
    AUTH = ""
    driver = ""
    session = ""

    def __init__(self,URI,AUTH,db):
        self.URI = URI
        self.AUTH = AUTH
        self.driver = GraphDatabase.driver(URI, auth=AUTH)
        self.session = self.driver.session(database=db)
        
    def check_if_node_present(self,tx,node):
        if node["type"] == "Car":
            result = tx.run("Match (n:Car) where n.Name=$name return n",name=node["Name"])
            return len([ele["n"] for ele in result])
            
        elif node["type"] == "Model":
            result = tx.run("Match (n:Model) where n.Name=$name return n",name=node["Name"])
            return len([ele["n"] for ele in result])
            
        elif node["type"] == "Possible_Problem":
            result = tx.run("Match (n:Possible_Problem) where n.name=$name return n",name=node["name"])
            return len([ele["n"] for ele in result])
        else:
            result = tx.run("Match (n:Problem) where n.desc=$name return n",name=node["desc"])
            return len([ele["n"] for ele in result])
            
    def check_if_relationship_present(self,tx,data):
        if data[1]["type"] == "Leads_to":
            res = tx.run("Match (n) where id(n)=$node1 Match (m) where id(m)=$node2 Match p = (n)-[r:"+str(data[1]["type"])+"]->(m) where r.relation=$rel AND r.weight=$weight  return p",node1=data[0],node2=data[2],rel=data[1]["name"],weight=data[1]["weight"])
            ans = [ele["p"] for ele in res]
            return len(ans)
        
        else:
            res = tx.run("Match (n) where id(n)=$node1 Match (m) where id(m)=$node2 Match p = (n)-[r:"+str(data[1]["type"])+"]->(m) where r.relation=$rel  return p",node1=data[0],node2=data[2],rel=data[1]["name"])
            ans = [ele["p"] for ele in res]
            return len(ans)
        
    def isLogicTreePresent(self,tx,data):
        car = data["Car"]
        model = data["Model"]
        tree = data["tree"].capitalize()
        
        
        if len([x["id"] for x in tx.run("Match (n:Car) where n.Name=$car return id(n) as id",car=car)]) != 0:
            if len([ele["id"] for ele in tx.run("Match (n:Car) where n.Name=$car Match (m:Model) where m.Name=$model Match (n)-[r:Model]->(m) return id(m) as id",car=car,model=model)]) != 0:
                ans = tx.run("Match (n:Model) where n.Name=$name  Match (n)-[r]->(m) where r.relation=$relation  return id(m) as id,r.relation as rel",name=model,relation=tree)
                temp = [e["id"] for e in ans]
                if len(temp) != 0:
                    return 0
                else:
                    return 1
            else:
                return 2
        else:
            return 2
       

    def getNodeId(self,tx,node):
        #print(node)
        if node["type"] == "Car":
            res = tx.run('Match (n:Car) where n.Name=$name return id(n) as id',name=node["Name"])
            return [ele["id"] for ele in res]
        if node["type"] == "Model":
            res = tx.run('Match (n:Model) where n.Name=$name return id(n) as id',name=node["Name"])
            return [ele["id"] for ele in res]
        if node["type"] == "Problem":
            res = tx.run('Match (n:Problem) where n.desc=$desc return id(n) as id',desc=node["desc"])
            return [ele["id"] for ele in res]
        if node["type"] == "Possible_Problem":
            res = tx.run('Match (n:Possible_Problem) where n.name=$name return id(n) as id',name=node["name"])
            return [ele["id"] for ele in res]
        else:
            return None
        
    def traverse(self,tx,node,l=[]): 
        l.append(node)
        result = tx.run("Match (n) where id(n)=$ids Match (n)-[r]->(m) return id(m) as id,r.relation as rel",ids=node)
        nodes = [[res["id"],res["rel"]] for res in result]
        if len(nodes) == 0:
            #print("exit")
            return 
        #print(nodes)
        for n in nodes:
            if n not in l:
                l.append(n[0])
                self.traverse(tx,n[0])
        
        return l 

    def traverse_(self,node):
        res = self.session.execute_read(self.traverse,node)
        print(set(res))


    def add_nodes(self,tx,node):
        if node["type"] == "Car":
            result = tx.run("Create (n:Car) SET n.Name=$name SET n.type=$type_ Return id(n) as id ",name=node["Name"],type_=node["type"])
            #print("Car Created")
            return result.single()[0]
            
        elif node["type"] == "Model":
            result = tx.run("Create (n:Model) SET n.Name=$name SET n.type=$type_ Return id(n) as id  ",name=node["Name"],type_=node["type"])
            #print("Model Created")
            return result.single()[0]
            
        elif node["type"] == "Possible_Problem":
            result = tx.run("Create (n:Possible_Problem) set n.name=$name SET n.type=$type_ Return id(n) as id ",name=node["name"],type_=node["type"])
            #print("PP Created")
            return result.single()[0]
        else:
            result = tx.run("Create (n:Problem) set n.desc=$desc SET n.type=$type_ Return id(n) as id ",desc=node["desc"],type_=node["type"])
            #print("Problem Created")
            return result.single()[0]
            
    def add_relationship(self,tx,data):
        print(data)
        node1 = data[0]
        node2 = data[1]
        node3 = data[2]
        rel_type = node2["type"]
        relation = node2["name"] 
        
        
        
        if "weight" in node2.keys():
            weight = node2["weight"]
            result = tx.run("Match (n) where id(n) = $node1 Match (m) where id(m) = $node3 Create (n)-[r:"+str(rel_type)+"]->(m) SET r.relation=$relation SET r.weight=$weight Return 'Relation Created'",node1=node1,node3=node3,relation=relation,weight=weight) 
            
            return result.single()[0]
        
        
        else:
            result = tx.run("Match (n) where id(n) = $node1 Match (m) where id(m) = $node3 Create (n)-[r:"+str(rel_type)+"]->(m) SET r.relation=$relation Return 'Relation Created'",node1=node1,node3=node3,relation=relation)
            
            return result.single()[0]


    def add_logic_tree(self,data,Model):
        node_set = []
        res = self.session.execute_read(self.isLogicTreePresent,Model)
        if res == 2:
            node1,node2 = None,None
            for i in data:
                #print(i)
                node1 = self.CreateNode(i[0],node_set)
                node_set.append(node1)
                node2 = self.CreateNode(i[2],node_set)
                node_set.append(node2)
                if self.session.execute_read(self.check_if_relationship_present,[node1,i[1],node2]) == 0:
                    res = self.session.execute_write(self.add_relationship,[node1,i[1],node2])
                else:
                    print("Relation already present ",[node1,i[1],node2])
                #print(res)
            print("Tree Created")
            return "Tree Created Successfully"
        elif res == 1:
            
            model = {}
            model["type"] = "Model"
            model["Name"] = Model["Model"]
            
            node = self.session.execute_read(self.getNodeId,model)
            node_set = self.session.execute_read(self.traverse,node[0])
            if node_set is None:
                node_set = []
            
            #print("set:",node_set)
            node1,node2 = None,None
            for i in data:
                #print(i)
                node1 = self.CreateNode(i[0],node_set)
                node_set.append(node1)
                node2 = self.CreateNode(i[2],node_set)
                node_set.append(node2)
                if self.session.execute_read(self.check_if_relationship_present,[node1,i[1],node2]) == 0:
                    res = self.session.execute_write(self.add_relationship,[node1,i[1],node2])
                else:
                    print("Relation already present ",[node1,i[1],node2])
            print("Tree Created")
            return "Tree Created Successfully"            
        else:
            print("Already Exist")
            return "Logic Tree Already Exist."

    def CreateNode(self,node,node_set):
        node1 = None
        #print(node)
        if self.session.execute_read(self.check_if_node_present,node) == 0:
            node1 = self.session.execute_write(self.add_nodes,node)
            return node1
        
        ele = self.session.execute_read(self.getNodeId,node)
        if node["type"] == "Problem":
            for e in ele:
                if e in node_set:
                    return e
                    
            node1 = self.session.execute_write(self.add_nodes,node)
            return node1
        
        
        return ele[0] 
        
        
    def CreateLogicTree(self,df,data):

        relations = []
        nodes = []
        car = []
        problem = []
        pp = []
        model = []
        all_pp = []
        for index, row in df.iterrows():
            node1 = row["Node1"].split(":",1)[0]
            name1 = row["Node1"].split(":",1)[1].strip().capitalize()
            node2 = row["Node2"].split(":",1)[0]
            name2 = row["Node2"].split(":",1)[1].strip().capitalize()
            
            
            if node1 == "Car" and node2 == "Model":
                n1 = {}
                n2 = {}
                r = {}
                n1["type"] = node1
                n1["Name"] = name1
                n2["type"] = node2 
                n2["Name"] = name2
                r["type"] = "Model"
                r["name"] = row['Relationship'].capitalize()
                relations.append([n1,r,n2]) 
            
            if node1 == "Model" and node2 == "Problem":
                n1 = {}
                n2 = {}
                r = {}
                n1["type"] = node1
                n1["Name"] = name1 
                n2["type"] = node2 
                n2["desc"] = name2 
                r["type"] = "Problem"
                r["name"] = row['Relationship'].capitalize()
                relations.append([n1,r,n2]) 
            
            if node1 == "Car" and node2 == "Problem":
                n1 = {}
                n2 = {}
                r = {}
                n1["type"] = node1
                n1["Name"] = name1 
                n2["type"] = node2 
                n2["desc"] = name2 
                r["type"] = "Problem"
                r["name"] = row['Relationship'].capitalize()
                relations.append([n1,r,n2])
            
            if node1 == "Problem" and node2 == "Problem":
                n1 = {}
                n2 = {}
                r = {}
                n1["type"] = node1
                n1["desc"] = name1.replace("\n"," ")
                n2["type"] = node2 
                n2["desc"] = name2.replace("\n"," ")
                r["type"] = "Problem"
                r["name"] = row['Relationship'].capitalize()
                relations.append([n1,r,n2]) 
                
              


            if node1 == "Problem" and node2 == "Possible_Problem":
                arr = name2.split('\n')
                for e in range(len(arr)):
                    if "%" not in arr[e]:
                        arr[e] = "% "+arr[e]
                for e in arr:
                    n1 = {}
                    n2 = {}
                    r = {}
                    n1["type"] = node1
                    n1["desc"] = name1.replace("\n","")
                    n2["type"] = node2 
                    n2["name"] = e.split("%")[1].strip().capitalize()
                    r["type"] = "Leads_to"
                    r["weight"] = str(e.split("%")[0])
                    r["name"] = row['Relationship']
                    relations.append([n1,r,n2]) 

            if node1 == "Model" and node2 == "Possible_Problem":
                arr = name2.split('\n')
                for e in range(len(arr)):
                    if "%" not in arr[e]:
                        arr[e] = "% "+arr[e]
                for e in arr:
                    n1 = {}
                    n2 = {}
                    r = {}
                    n1["type"] = node1
                    n1["Name"] = name1 
                    n2["type"] = node2 
                    n2["name"] = e.split("%")[1].strip().capitalize()
                    r["type"] = "Leads_to"
                    r["weight"] = str(e.split("%")[0])
                    r["name"] = row['Relationship']
                    relations.append([n1,r,n2])            
            
            
            
            
            if node1 == "Car" and name1 not in car:
                ele = {}
                ele["type"] = node1
                ele["Name"] = name1
                nodes.append(ele)
                car.append(name1)
                
            if node1 == "Model" and name1 not in model:
                ele = {}
                ele["type"] = node1
                ele["Name"] = name1
                nodes.append(ele)
                model.append(name1)
                
            if node1 == "Possible_Problem":
                arr = name1.split('\n')
                for e in range(len(arr)):
                    if "%" not in arr[e]:
                        arr[e] = "% "+arr[e]
                for e in arr:
                    if e.split("%")[1].strip().capitalize() not in pp:
                        ele = {}
                        ele["type"] = node1
                        ele["name"] = e.split("%")[1].strip().capitalize()
                        nodes.append(ele)
                        pp.append(e.split("%")[1].strip().capitalize())
                
                
            if node1 == "Problem" and name1 not in problem:
                ele = {}
                ele["type"] = node1
                ele["desc"] = name1.replace("\n","")
                nodes.append(ele)
                problem.append(name1)
                
            if node2 == "Car" and name2 not in car:
                ele = {}
                ele["type"] = node2
                ele["Name"] = name2
                nodes.append(ele)
                car.append(name1)
            if node2 == "Model" and name2 not in model:
                ele = {}
                ele["type"] = node2
                ele["Name"] = name2
                nodes.append(ele)
                model.append(name2)
                
                
            if node2 == "Possible_Problem":
                arr = name2.split('\n')
                for e in range(len(arr)):
                    if "%" not in arr[e]:
                        arr[e] = "% "+arr[e]
                for e in arr:
                    all_pp.append(e.split("%")[1].strip().capitalize())
                    if e.split("%")[1].strip().capitalize() not in pp:
                        ele = {}
                        ele["type"] = node2
                        ele["name"] = e.split("%")[1].strip().capitalize()
                        nodes.append(ele)
                        pp.append(e.split("%")[1].strip().capitalize())
                
            if node2 == "Problem" and name2 not in problem:
                ele = {}
                ele["type"] = node2
                ele["desc"] = name2.replace("\n","")
                nodes.append(ele)
                problem.append(name2)



        res_ = self.add_logic_tree(relations,{"Car":data[0],"Model":data[1],"tree":data[2]})
        
        print("Done")
        return res_
    
    #---------------------------------------
    def getLogicTree_(self,tx,data):
        res = tx.run("Match (n:Model) where n.Name=$model Match (n)-[r]->(m) where r.relation=$rel return id(m) as id,m.type as node_type,m.desc as node_desc,r.relation as rel",model=data["Model"],rel=data["tree"]) 
        ans = [[ele["id"],ele["rel"],ele["node_type"],ele["node_desc"]] for ele in res][0]
        return {"id":ans[0],"Question":ans[3]}
        
    def getLogicTree(self,data):
        '''
        data = {}
        data["Car"] = "Dodge"
        data["Model"] = "Grand caravan"
        data["tree"] = "No heat from heater"
        '''
        res = self.session.execute_read(self.isLogicTreePresent,data)
        if res == 0:
            res = self.session.execute_read(self.getLogicTree_,data)
            qid = res["id"]
            res_ = self.getPossibleCause(qid)
            res["Possible_Problem"] = res_
            return res
        else:
            return {"message":"No Logic Tree Present"}
    #----------------------------------------
    
    #----------------------------------------
    def getPossibleCause_(self,tx,node_id):
        res = tx.run("Match (n) where id(n)=$nodeId Match (n)-[r]->(m) where r.relation=$pp return id(m) as id,m.type as node_type,m.name as node_pp,r.relation as rel,r.weight as weight",nodeId=int(node_id),pp="Possible_Problem")
        arr = [{"id":ele["id"],"name":ele["node_pp"],"weight":ele["weight"]} for ele in res]
        ans = {}
        for i in arr:
            ans[i["name"]] = i["weight"]
        return ans
        
        
    def getPossibleCause(self,nodeid):
        res = self.session.execute_read(self.getPossibleCause_,nodeid)  
        return res        
        
    #----------------------------------------
    def getNextProblem_(self,tx,data):
        node_id = data[0]
        res = tx.run("Match (n) where id(n)=$nodeId Match (n)-[r]->(m) return id(m) as id,m.type as node_type,m.desc as node_desc,m.name as node_pp,r.relation as rel,r.weight as weight",nodeId=node_id)
        return [[ele["id"],ele["rel"],ele["node_type"],ele["node_desc"],ele["node_pp"],ele["weight"]] for ele in res]
    def getNextProblem(self,nodeid,rel):
        res = self.session.execute_read(self.getNextProblem_,[int(nodeid)])
        arr = []
        for ele in res:
            e = {}
            if ele[2] == "Possible_Problem" and ele[3] is None:
                e["id"] = ele[0]
                e["Type"] = "Possible_Problem"
                e["Node"] = ele[4]
                e["Relation"] = ele[1]
                e["weight"] = ele[5]
            else:
                e["id"] = ele[0]
                e["Type"] = "Problem"
                e["Node"] = ele[3]
                e["Relation"] = ele[1]
            arr.append(e)
        ans = {} 
        
        for ele in arr:
            
            if ele["Relation"] != "Possible_Problem":    
                if ele["Relation"] in ans.keys():
                    e = {}
                    if ele["Type"] == "Possible_Problem":
                        e["weight"] = ele["weight"]
                    e["Node"] = ele["Node"]
                    e["id"] = ele["id"]
                    e["Type"] = ele["Type"]
                    ans[ele["Relation"]].append(e)
                else:
                    ans[ele["Relation"]] = []
                    e = {}
                    if ele["Type"] == "Possible_Problem":
                        e["weight"] = ele["weight"]
                    e["Node"] = ele["Node"]
                    e["id"] = ele["id"]
                    e["Type"] = ele["Type"]
                    ans[ele["Relation"]].append(e)
               
        print(ans)
        for k,v in ans.items():
           
            ele = {}
            
            for e in v:
          
                #pp
                if e["Type"] == "Possible_Problem":
                    #print(ele,"Possible_Problem" in ele.keys())
                    if "Possible_Problem" in ele.keys():
                        ele[e["Type"]].append({"id":e["id"],"Name":e["Node"],"Weigth":e["weight"]})
                    else:
                        ele[e["Type"]] = [{"id":e["id"],"Name":e["Node"],"Weigth":e["weight"]}]
                #p
                if e["Type"] == "Problem":
                    if "Problem" in ele.keys():
                        ele[e["Type"]].append({"id":e["id"],"Name":e["Node"]})
                    else:
                        ele[e["Type"]] = [{"id":e["id"],"Name":e["Node"]}]
                #print(ele)
            #print("---------")
            ans[k] = ele
                
        print(ans)
        for k,v in ans.items():
            for key,value in v.items():
                ele = {}
                if key == "Possible_Problem":
                    for e in value:
                        ele[e["Name"]] = e["Weigth"]
                    v[key] = ele
        
        return ans
     
    def getLogicTrees_(self,tx,model):
        res = tx.run("Match (n:Model) where n.Name=$model Match (n)-[r]->() return r.relation as rel",model=model)
        ans = [ele["rel"] for ele in res]
        return ans
        
    def getLogicTrees(self,model):
        res = self.session.execute_read(self.getLogicTrees_,model)
        return res
        
    def get_all_car_make(self,tx):
        res = tx.run("Match (n:Car) return n.Name as Name")
        ans = [ele["Name"] for ele in res]
        return ans
    def Cars(self):
        res = self.session.execute_read(self.get_all_car_make)
        return res 
        
    def get_models_for_carMake(self,tx,make):
        res = tx.run("Match (n:Car) where n.Name=$make Match (n)-[:Model]->(m) return m.Name as Name",make=make)
        ans = [ele["Name"] for ele in res]
        return ans
        
    def getModel(self,make):
        res = self.session.execute_read(self.get_models_for_carMake,make)
        return res
        
        




                
                