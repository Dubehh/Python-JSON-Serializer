import json
from abc import abstractmethod
from typing import Dict, Type


class JSONSerializable(dict):

    def __init__(self):
        super().__init__()
        self.__dict__ = self

    def serialize(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)


class JSONDeserializable:

    @abstractmethod
    def get_child_object_types(self) -> Dict[str, Type[JSONSerializable]]:
        pass


class JSONInterpreter:

    @staticmethod
    def parse_dict(json_str: str):
        dictionary = json.loads(json_str)
        return dictionary

    @staticmethod
    def read(dictionary: dict, root: JSONSerializable):
        for key, value in dictionary.items():
            if isinstance(value, list) and isinstance(root, JSONDeserializable):

                child_type = root.get_child_object_types()[key]
                root_child_list = getattr(root, key, [])

                for child in value:
                    child_instance = child_type()
                    parsed_child_instance = JSONInterpreter.read(child, child_instance)
                    root_child_list.append(parsed_child_instance)

                setattr(root, key, root_child_list)
            else:
                setattr(root, key, value)

        return root

