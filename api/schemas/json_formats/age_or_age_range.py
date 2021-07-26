from typing import Union
import strawberry

@strawberry.input
class AgeInputType:
    age: int
    start: int
    end: int

@strawberry.type
class AgeRange:
    start: str
    end: str

@strawberry.type
class Age:
    age: str

def filter_age_union(instance, input: AgeInputType):
    age = int(input.get("age"))
    start = int(input.get("start"))
    end = int(input.get("end"))
    if isinstance(instance, Age):
        if age != None and instance.age == age:
            return True
    if isinstance(instance, AgeRange):
        if start != None and end != None and start >= instance.start and end <= instance.end:
            return True
    if age == None and start == None and end == None:
        return True
    return False