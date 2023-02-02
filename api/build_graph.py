import os
import sys

api_folder = os.path.dirname(__file__)
aia_flow_folder = os.path.abspath(os.path.join(api_folder, os.pardir))
sys.path.append(aia_flow_folder)

from backend.aia.NENV import *
from backend.aia.main.utils import Coordinator

init_node_env()
coordinator = Coordinator()
coordinator.auto_loading()

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
        aia_json = request.json
        coordinator.load(aia_json)

        print("Loading success!")

        coordinator.updating_all_of_nodes()

        return {"build_status":"succeeded"}
    except Exception as e:
        print(e)
        return {"build_status":"failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)