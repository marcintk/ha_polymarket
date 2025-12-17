""" PolyMarket Miscellaneous Utilities """

import json

from .const import LOGGER

def parse_float_if(condition: bool, holder:dict, name:str, default=0.0, root="n/a") -> float:
    return parse_float(holder, name, default, root) if condition else default

def parse_float(holder:dict, name:str, default=0.0, root="n/a") -> float:
    try:
        if name in holder:
            return float(holder[name])
        else:
            LOGGER.warn(f"Attributte {name} not found for {root}")
    except:
        return default

    return default

def parse_float_from_list_if(condition: bool, holder:dict, name:str, index:int=0, default:float=0.0, root="n/a") -> float:
    return parse_float_from_list(holder, name, index, default, root) if condition else default

def parse_float_from_list(holder:dict, name:str, index:int=0, default:float=0.0, root="n/a") -> float:
    try:
        if name in holder:
            json_value = holder[name]
            collection = json.loads(json_value)

            if type(collection) == list:
                if index < len(collection):
                    return float(collection[index])
                else:
                    LOGGER.warn(f"Attribute {name} has no valid number of items in {collection}!")
            else:
                LOGGER.warn(f"Attribute {name} is not a collection {json_value}!")
        else:
            LOGGER.warn(f"Attribute {name} not found for {root}!")
    except Exception as e:
        LOGGER.warn(f"Attribute {name} exceptioned {e}!")

        return default

    return default

