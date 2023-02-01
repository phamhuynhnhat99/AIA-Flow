import os
import sys
import json

from ..flow.flow import Flow

class Coordinator:

    def __init__(self):

        self.title = os.environ["TITLE"]
        self.version = os.environ["VERSION"]

        # Topo
        self.flow = Flow()

        # all of nodes that may be used
        self.no_gui_nodes = []

        # all of directions
        self.arrows = []
        self.locations = dict() # example: self.locations[(0, 1)] = 1 means vertex 1 were connected with 0 via port 1

        # Contain nodes that are registered from self.no_gui_nodes
        self.registered_nodes = dict() # key = gid, value = Node

        # Toposort Result
        self.order = []

    
    def auto_loading(self):
        """ Load all of nodes that from aia.main.auto_loading folder """
        auto_loading_path = os.path.join(os.path.dirname(__file__), "no_gui_nodes")
        auto_loading_nodes = os.listdir(auto_loading_path)

        try:
            auto_loading_nodes.remove("__pycache__")
        except:
            None
        for aln in auto_loading_nodes:
            aln_path = os.path.join(auto_loading_path, aln)
            sys.path.append(aln_path)
            aln_nodes = aln + "_nodes.py"
            nodes_py = os.path.join(aln_path, aln_nodes)
            try:
                module_name = os.path.basename(nodes_py).split(".py")[0]
                self.no_gui_nodes += __import__(module_name).export_nodes
            except:
                continue


    def display_no_gui_nodes(self):
        print("-oOo-         All of nodes         -oOo-")
        for i, node_class in enumerate(self.no_gui_nodes):
            print("    Index:", i, "   ", node_class.title)

    
    def display_registered_nodes(self):
        for gid, node in self.registered_nodes.items():
            print("    id:", gid, "   ", node.__class__.title)


    def display_arrows(self):
        for arrow in self.arrows:
            print("          ", arrow[0], '---->', arrow[1], 'at (', self.locations[(arrow[0], arrow[1])], ')')

    
    def display_order(self):
        if self.order != []:
            print(self.order)
        else:
            print("This is not a DAG")

    
    def updating_toposort(self):
        tmp_vertices = list(self.registered_nodes.keys())
        self.flow.update_graph(vertices=tmp_vertices, arrows=self.arrows)
        self.order = self.flow.toposort()

    
    def updating_a_registered_node(self, u):
        """ get its descendants and "update_event" all of them """
        if u in self.registered_nodes.keys():
            self.registered_nodes[u].does_it_use_old_output = False
            genealogy_of_u = self.flow.sub_toposort_from(u)
            for v in genealogy_of_u:
                self.registered_nodes[v].update_event()

    
    def updating_all_of_nodes(self):
        for v in self.order:
            self.registered_nodes[v].update_event()


    def registering_a_new_node(self, ind):
        if 0 <= ind and ind < len(self.no_gui_nodes):
            new_node = self.no_gui_nodes[ind]()
            self.registered_nodes[new_node.global_id] = new_node
            self.updating_toposort()
            

    def registering_a_new_arrow(self, u, v, ind):
        if u in self.registered_nodes.keys() and v in self.registered_nodes.keys():

            if ind in self.registered_nodes[v].nodeinputs.keys():
                if self.registered_nodes[v].nodeinputs[ind] is not None:
                    old_u = self.registered_nodes[v].nodeinputs[ind].global_id
                    self.arrows.remove([old_u, v])
                    del self.locations[(old_u, v)]
                del self.registered_nodes[v].nodeinputs[ind]

            if ind in self.registered_nodes[v].nodevalueinputs.keys():
                del self.registered_nodes[v].nodevalueinputs[ind]

            if u != v:
                if [u, v] not in self.arrows:
                    self.arrows.append([u, v])
                    self.locations[(u, v)] = ind
                    self.registered_nodes[v].nodeinputs[ind] = self.registered_nodes[u]

                    self.updating_toposort()


    def save(self, aia_save):
        aia = dict()

    
    def load(self, aia_load):

        self.title = os.environ["TITLE"]
        self.version = os.environ["VERSION"]
        self.flow = Flow()
        self.arrows = []
        self.locations = dict()
        self.registered_nodes = dict()
        self.order = []

        no_gui_nodes_className = [node.className for node in self.no_gui_nodes]
        print(no_gui_nodes_className)
        with open(aia_load) as json_file:
            aia = json.load(json_file)
            elements = aia["elements"]
            for element in elements:
                if element["type"] != "default": # is node
                    node = element
                    ind = no_gui_nodes_className.index(node["type"])
                    new_node = self.no_gui_nodes[ind]()
                    new_node.global_id = node["id"]
                    if node["type"] == "textInputNode":
                        new_node.text = node["data"]["text"]
                    
                    self.registered_nodes[new_node.global_id] = new_node
                else: # is edge
                    edge = element
                    u = edge["source"]
                    v = edge["target"]
                    ind = int(edge["targetHandle"].split("_inp_")[-1])
                    self.arrows.append([u, v])
                    self.locations[(u, v)] = ind
                    self.registered_nodes[v].nodeinputs[ind] = self.registered_nodes[u]
            
            self.updating_toposort()
            
            json_file.close()


class export_widgets:

    Coordinator = Coordinator