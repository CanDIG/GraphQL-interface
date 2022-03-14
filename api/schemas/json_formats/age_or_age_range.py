from api.interfaces.input import Input
from typing import Optional
from api.schemas.utils import set_field
import strawberry

@strawberry.input
class AgeInputType(Input):
    age: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None

@strawberry.type
class Age:
    age: str

    @staticmethod
    def deserialize(json):
        return Age(**json)

    @staticmethod
    def filter(instance, input: AgeInputType):
        return filter_age(instance, input)

@strawberry.type
class AgeRange:
    start: Age
    end: Age

    @staticmethod
    def deserialize(json):
        ret = AgeRange(**json)

        set_field(json, ret, 'start', Age)
        set_field(json, ret, 'end', Age)

        return ret

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