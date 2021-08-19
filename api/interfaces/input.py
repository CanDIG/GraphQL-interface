class Input:
    def __hash__(self) -> int:
        lst = []
        for attr in input.__annotations__:
            lst.append(input.__getattribute__(attr))
        return hash(tuple(lst))