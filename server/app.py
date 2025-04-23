from flask import Flask, request, jsonify, make_response
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import time, pymongo, json

# import config file
with open("config.json", "rb") as f:
    configData = json.load(f)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SECRET_KEY"] = configData["secretKey"]
socketio = SocketIO(app, cors_allowed_origins="*")

# connect to mongo db
db = pymongo.MongoClient(configData["dbUrl"])["chat"]
col = db["messages"]

@app.route("/")
def index():
    return ""

# returns the recent messages
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


# receives a message from the client,
# inserts into the database,
# and sends the message to all connected clients
@socketio.on("message")
def handle_message(json):
    now = int(time.time())
    json["time"] = now
    col.insert_one(dict(json))
    print(json)
    socketio.emit("messageResp", json)

if __name__=="__main__":
    socketio.run(app, debug=True, port=999)