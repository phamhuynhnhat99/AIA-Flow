from aia.NENV import *

widgets = import_widgets(__file__) # optional

class TextNodeBase(Node):
    path = "text/text_nodes" # compulsory

    def __init__(self):
        super().__init__()
        self.output = None

    
    def get_output(self):
        return self.get_text()


    def update_event(self):
        self.output = self.get_output()
        self.nodevalueoutput_[0] = self.output


class textInputNode(TextNodeBase):
    className = "textInputNode"
    title = "Text Input"

    def __init__(self):
        super().__init__()
        self.title = "Text Input"
        self.text = ''


    def set_tilte(self, tilte):
        self.title = tilte

    
    def get_text(self):

        if self.text == "":
            output = 0
        else:
            output = self.text
        return output


# compulsory
export_nodes = [
   textInputNode,

]