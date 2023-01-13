
from .Base import Base

class Node(Base):

    def __init__(self, num_inp=0, num_out=1, title=''):
        
        super().__init__()

        self.num_inp = num_inp
        self.num_out = num_out
        self.title = title

        self.version: str = None

        self.nodevalueoutput_ = dict()
        # if self.num_inp == 0:
        #     self.nodevalueoutput_[0] = self.get_output()
        self.nodeoutput_ = None

        self.nodevalueinputs = dict() # dict of dict
        self.nodeinputs = dict() # dict of dict

        for ind in range(self.num_inp):
            self.nodevalueinputs[ind] = None
            self.nodeinputs[ind] = None
        

    # nodevalueinputs
    def update_nodevalueinputs(self):
        self.nodevalueinputs = dict()
        for ind, node in self.nodeinputs.items():
            if node is not None:
                value = node.nodevalueoutput_
                self.nodevalueinputs[ind] = value
            else:
                self.nodevalueinputs[ind] = None


    def get_nodevalueinputs(self, ind = -1):
        if ind == -1:
            return self.nodevalueinputs
        elif ind in self.nodevalueinputs.keys():
            return self.nodevalueinputs[ind]
        return None


    def remove_nodeinputs_and_its_value(self, node):
        if node in self.nodeinputs.values():
            ind = list(self.nodeinputs.values()).index(node)
            key = list(self.nodeinputs.keys())[ind]
            del self.nodeinputs[key]
            if key in self.nodevalueinputs.keys():
                del self.nodevalueinputs[key]


    """ RESET """
    def reset(self):
        self.title = ''
        self.version: str = None

        self.nodevalueinputs = dict()

        self.nodevalueoutput_ = dict()

        self.nodeinputs = dict()