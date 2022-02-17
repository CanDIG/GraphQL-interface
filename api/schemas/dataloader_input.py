class DataLoaderInput:
    def __init__(self, token, ids=None, page_number=None):
        self.token = token
        if page_number == None:
            self.page_number = 1
        else:
            self.page_number = page_number
        if ids:
            self.ids = frozenset(ids)
        else:
            self.ids = frozenset()

    def __hash__(self):
        return hash((self.token, self.ids))

    def __eq__(self, o: object) -> bool:
        return self.token == o.token and self.ids == o.ids

class DataLoaderOutput:
    def __init__(self, output):
        self.output = output
