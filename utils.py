""" PolyMarket Miscellaneous Utilities """

import json

from .const import LOGGER

def parse_str(holder: dict, name: str, default: str = "n/a", root: str = "n/a", required: bool = False) -> str:
    return parse_value(holder, name, default, as_type=str, root=root, required=required)

def parse_float(holder: dict, name: str, default: float = 0.0, root: str = "n/a", required: bool = False) -> float:
    return parse_value(holder, name, default, as_type=float, root=root, required=required)

def parse_float_from_list(holder:dict, name:str, index:int=0, default:float=0.0, root:str="n/a", required:bool=False) -> float:
    if name in holder:
        try:
            json_value = holder[name]
            collection = json.loads(json_value)

            if type(collection) == list:
                if index < len(collection):
                    return float(collection[index])
                else:
                    LOGGER.warning(f"List attribute '%s' has no valid number of items in '%s'!", name, collection)
            else:
                LOGGER.warning(f"Attribute '%s' is not a collection '%s'!", name, json_value)
        except Exception as e:
            LOGGER.warning("List attribute '%s' exceptioned: %s!", name, e)
            return default

    elif required:
        LOGGER.warning(f"List attribute '%s' not found for '%s'!", name, root)

    return default

def parse_value(holder: dict,
                name: str,
                default=None,
                as_type=str,
                root: str = "not-provided",
                required: bool = False):
    if name in holder:
        try:
            return as_type(holder.get(name))
        except Exception:
            LOGGER.error("Failed to convert attribute '%s', returning default=%s.", name, default)
    elif required:
        LOGGER.warning("Attribute '%s' not found for '%s', returning default=%s.", name, root, default)

    return default