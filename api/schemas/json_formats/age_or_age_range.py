from api.interfaces.input import Input
from typing import Optional
import strawberry

@strawberry.input
class AgeInputType(Input):
    age: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None

@strawberry.type
class AgeRange:
    start: str
    end: str

    @staticmethod
    def filter(instance, input: AgeInputType):
        return filter_age(instance, input)


@strawberry.type
class Age:
    age: str

    @staticmethod
    def filter(instance, input: AgeInputType):
        return filter_age(instance, input)

def filter_age(instance, input: AgeInputType):
    age = int(input.age)
    start = int(input.start)
    end = int(input.end)

    if isinstance(instance, Age):
        if age != None and instance.age == age:
            return True
    
    if isinstance(instance, AgeRange):
        if start != None and end != None and start >= instance.start and end <= instance.end:
            return True
    
    if age == None and start == None and end == None:
        return True
    
    return False