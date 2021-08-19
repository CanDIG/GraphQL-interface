class DataLoaderInput:
    def __init__(self, token, ids):
        self.token = token
        self.ids = ids

    def __hash__(self):
        return hash((self.token, self.ids))

    def __eq__(self, o: object) -> bool:
        return self.token == o.token and self.ids == o.ids

class DataLoaderOutput:
    def __init__(self, output):
        self.output = output