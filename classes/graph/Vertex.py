class Vertex(object):


    def __init__(self, value, name=None):
        self.value = value
        self.name = name
        self.inputs = set()
        self.outputs = set()


    def get_value(self):
        return self.value


    def set_value(self, value):
        self.value = value


    def get_name(self):
        return self.name


    def add_input(self, edge):
        self.inputs.add(edge)


    def get_inputs(self, edge):
        return self.inputs


    def add_output(self, edge):
        self.outputs.add(edge)


    def get_outputs(self, edge):
        return self.outputs

