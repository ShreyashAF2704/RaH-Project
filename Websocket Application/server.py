'''
from flask import Flask
from flask_socketio import SocketIO,emit

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('connect')
def connect(data):
    print(data)
    emit('response',{'from':'server'})

@socketio.on('validate')    
def validate(req):
    print(req)
    emit('return_validate',"Validation Successful")

@socketio.on('converse')
def converse(Message):
    print(Message)
    emit('return_converse','Hello')

@socketio.on('disconnect')
def disconnect(message):
    print(message)
    emit('return_disconnect','Bye Bye')


if __name__ == '__main__':
    socketio.run(app,port=3000,debug=True)

'''
#Async Socket Server
#from flask import Flask
from aiohttp import web
import socketio
import time
from neo4j import GraphDatabase
URI = "bolt://localhost:7687/"
AUTH = ("shreyash", "1234")
driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session(database="demo2")

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

ip_allowed = ['127.0.0.1']


#-----

def get_car_data(tx):
    result = tx.run("""
             MATCH (n:Car) return n
             """)
    record = list(result)
    return record

   
#get relation's from node
def get_relations(tx,data):
    type_node = data["Type"]
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
    
    
def fetch_relation_for_node(data):
    #data = {}
    #data["type"] = "Problem"
    #data["desc"] = 'Does it turn Over?'
    rel = session.execute_read(get_relations,data)
    ans = []

    for i in rel:
        ans.append( [i.data()["r"][1],i.data()["r"][2] ])
    return ans
    #print(ans)       
#-----

@sio.event
async def connect(sid, environ):
    if environ["REMOTE_ADDR"] not in ip_allowed:
        print(environ["REMOTE_ADDR"],' trying to connect.')
        await sio.emit('forceDisconnect','Not allowed to connect.')
    else:
        print("connect ", sid)

@sio.event
async def login(sid,data):
    time.sleep(4)
    cars = fetch_cars()
    msg = "Select The Car"
    await sio.emit('next',{"msg":msg,"data":cars})

@sio.event
async def get_data(sid,data):
    #print(data)
    node_data = {}
    prev_ques = ""
    if data["node"]["Type"] == "Car":
        node_data["Type"] = "Car"
        node_data["Name"] = data["node"]["Name"]
        prev_ques = data["node"]["Name"]
    if data["node"]["Type"] == "Problem":
        node_data["Type"] = "Problem"
        node_data["desc"] = data["node"]["desc"]
        prev_ques = data["node"]["desc"]
    res =  fetch_relation_for_node(node_data)

    if len(res) == 0:
         await sio.emit(f'return_data',{'question':"No Further Data Found.Type 1 to exit.",'data':res})
    else:
        pp = "Possible Problems: \n"
        ans = []
        pp_dict = {}
        problem_count = 0
        for i in res:
            if i[0] == "Possible_Problem":
                #print("PP:",i[1])
                pp += i[1]["name"]+"\n"
            elif i[0] != "Possible_Problem" and i[1]["Type"] == "Possible_Problem":
                if i[0] not in pp_dict.keys():
                    pp_dict[i[0]] = i[1]["name"]
                else:
                    pp_dict[i[0]] += "\n"+i[1]["name"]
            else:
                ans.append(i)
                problem_count +=1 
        if len(ans) == 0:
            for k,v in pp_dict.items():
                ans.append([k,v])
            await sio.emit('result_conversation',{'question':prev_ques+"\n"+pp,'data':ans})
        else:
            time.sleep(4)
            await sio.emit(f'return_data',{'question':prev_ques+"\n"+pp,'data':ans})


@sio.event
async def my_response(sid,data):
    print(f"[{sid}]] :{data}")

    time.sleep(4)
    await sio.emit(f'disconnectNow','You can disconnect now.')




@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    #app.run(port=5050)
    web.run_app(app)
    print(sio.sid)