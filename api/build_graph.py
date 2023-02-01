import os

from ..backend.aia.NENV import *
from ..backend.aia.main.utils import Coordinator

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
        aia = request.json

        coordinator.reset_all_ignore_no_gui_nodes()
        no_gui_nodes_className = [node.className for node in coordinator.no_gui_nodes]

        elements = aia["elements"]
        nodes = []
        edges = []
        for element in elements:
            if element["type"] != "default": # is node
                nodes.append(element)
            else:
                edges.append(element)

        for node in nodes:
            ind = no_gui_nodes_className.index(node["type"])
            try:
                new_node = coordinator.no_gui_nodes[ind]()
            except Exception as e:
                print(e)
                continue
            new_node.global_id = node["id"]
            if node["type"] == "textInputNode":
                new_node.text = node["data"]["text"]
            coordinator.registered_nodes[new_node.global_id] = new_node
        
        for edge in edges:
            u = edge["source"]
            v = edge["target"]
            ind = int(edge["targetHandle"].split("_inp_")[-1])
            coordinator.arrows.append([u, v])
            coordinator.locations[(u, v)] = ind
            coordinator.registered_nodes[v].nodeinputs[ind] = coordinator.registered_nodes[u]
        
        coordinator.updating_toposort()
        coordinator.updating_all_of_nodes()

        return {"build_status":"succeeded"}
    except Exception as e:
        print(e)
        return {"build_status":"failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)