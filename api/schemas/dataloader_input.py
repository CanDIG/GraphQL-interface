class DataLoaderInput:
    def __init__(self, token, ids, input):
        self.token = token
        self.ids = ids
        self.input = input

class DataLoaderOutput:
    def __init__(self, output):
        self.output = output