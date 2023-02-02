import os
import sys

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
        """ Load all of nodes that from aia.main.no_gui_nodes folder """

        script_dir = os.path.dirname(__file__) # backend.aia.main folder
        no_gui_nodes_path = os.path.join(script_dir, "no_gui_nodes")

        list_of_nodes = os.listdir(no_gui_nodes_path)
        for node in list_of_nodes:
            my_module_dir = os.path.join(no_gui_nodes_path, node)
            sys.path.append(my_module_dir)
            node_name = node + "_nodes"
            try:
                self.no_gui_nodes += __import__(node_name).export_nodes
            except Exception as e:
                print(e)

        self.no_gui_nodes_className = [node.className for node in self.no_gui_nodes]


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

    
    def reset_all_ignore_no_gui_nodes(self):
        self.title = os.environ["TITLE"]
        self.version = os.environ["VERSION"]
        self.flow = Flow()
        self.arrows = []
        self.locations = dict()
        self.registered_nodes = dict()
        self.order = []

    
    def load(self, aia_json):
        self.reset_all_ignore_no_gui_nodes()

        elements = aia_json["elements"]
        for element in elements:
            if element["type"] != "default": # is node
                node = element
                ind = self.no_gui_nodes_className.index(node["type"])
                try:
                    new_node = self.no_gui_nodes[ind]()
                except Exception as e:
                    print(e)
                    continue
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


class export_widgets:

    Coordinator = Coordinator