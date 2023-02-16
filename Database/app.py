from flask import Flask, jsonify, request
from flask_session import Session
import pandas as pd
from neo4j import GraphDatabase
from Neo4jDB import Neo4jDB

app = Flask(__name__)
app.secret_key = "12344"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

URI = "bolt://neo4j-nlb-e0ad87a85a310b86.elb.us-east-1.amazonaws.com:7687/"
Auth = ("neo4j", "dbadmin@123")
database = "Neo4j"


@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        data = "hello world"
        resp = jsonify(success=True)
        return resp


@app.route('/healthcheck',methods=['GET'])
def health():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route('/addLogicTree',methods=['POST'])
def addLogicTree():
    file = request.files['file']
    car = request.form["Car"].capitalize()
    model = request.form["Model"].capitalize()
    problem = request.form["Problem"].capitalize()
    df = pd.read_excel(file)
    db = Neo4jDB(URI,Auth,database)
    res = db.CreateLogicTree(df,[car,model,problem])
    print(df)
    print([car,model,problem])
    return jsonify({"message":"Uploaded Successfully","success":True,"response":res})

@app.route('/getNext/<int:Node_id>',methods=['GET'])
def getNext(Node_id):
    #nodeId = int(request.params["Node_id"])
    db = Neo4jDB(URI,Auth,database)
    res = db.getNextProblem(Node_id,"")
    return jsonify(data=res)
   
@app.route('/logicTree',methods=['GET'])
def getLogictree() :
    model = request.args.get('model')
    db = Neo4jDB(URI,Auth,database)
    res = db.getLogicTrees(model)
    return jsonify(data=res)
    
if __name__ == '__main__':
    app.run(port=3000,debug=True)