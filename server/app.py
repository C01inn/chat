from flask import Flask, request, jsonify, make_response
from flask_socketio import SocketIO
from flask_cors import CORS
import time, pymongo, json

# import config file
#with open("config.json", "rb") as f:
#    configData = json.load(f)
configData = {
    "secretKey": "rfyky4f6wslklcxhxra86xlovsg8nu",
    "dbUrl": "mongodb://admin:8268Wrenfield@musicapp-shard-00-00.czdvw.azure.mongodb.net:27017,musicapp-shard-00-01.czdvw.azure.mongodb.net:27017,musicapp-shard-00-02.czdvw.azure.mongodb.net:27017/chat?ssl=true&replicaSet=atlas-88n74b-shard-0&authSource=admin&retryWrites=true&w=majority"
}

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = configData["secretKey"]
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
socketio = SocketIO(app, cors_allowed_origins="*")

db = pymongo.MongoClient(configData["dbUrl"])["chat"]
col = db["messages"]

@app.route("/")
def index():
    return ":)"

@app.route("/last/<number>")
def last(number):
    data = sorted(list(col.find()), key=lambda k: k["time"])
    number = 0-int(number)
    data = data[number:]
    for x in data:
        x["_id"] = ''
    # make response
    resp = make_response(json.dumps(data))
    resp.headers["content-type"] = 'application/json'
    return resp

@app.route('/myip', methods=["GET"])
def myip():
    clientIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return jsonify({"ip": clientIp})

@socketio.on("message")
def handle_message(json, methods=["GET", "POST", "PUT"]):
    now = int(time.time())
    json["time"] = now
    json["ip"] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    col.insert_one(dict(json))
    print(json)
    socketio.emit("messageResp", json)

if __name__=="__main__":
    socketio.run(app, debug=True, port=999)