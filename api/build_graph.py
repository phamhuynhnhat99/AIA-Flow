import os

from ..backend.aia.NENV import *
from ..backend.aia.main.utils import Coordinator

init_node_env()
coordinator = Coordinator()
coordinator.auto_loading()

import json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/build_graph", methods=['POST'])
def build_graph():
    try : 
        print(request.data,request.json)
        data = request.json
        print(data)
        out_file = open("temp_graph.json", "w")
        json.dump(data, out_file, indent = 6)
        out_file.close()
        coordinator.load("temp_graph.json")
        coordinator.updating_all_of_nodes()
        return {"build_status":"succeeded"}
    except:
        return {"build_status":"failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)