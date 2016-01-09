class Vertex(object):


    def __init__(self, name=None, value=None, domain=None):
        self.name = name
        self.value = value
        self.domain = domain
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


    def remove_input(self, edge):
        self.inputs.remove(edge)


    def remove_output(self, edge):
        self.outputs.remove(edge)


    def get_inputs(self):
        return self.inputs


    def clear_inputs(self):
        self.inputs.clear()


    def clear_outputs(self):
        self.outputs.clear()


    def add_output(self, edge):
        self.outputs.add(edge)


    def get_outputs(self):
        return self.outputs

