from typing import Dict, Type

from serialization import JSONSerializable, JSONDeserializable, JSONInterpreter


class Root(JSONSerializable, JSONDeserializable):

    def __init__(self):
        super().__init__()

        self.id = 1
        self.name = "root"
        self.foo = True
        self.children = []
        self.grand_children = []

    def get_child_object_types(self) -> Dict[str, Type[JSONSerializable]]:
        return {
            "children": Child,
            "grand_children": GrandChild
        }


class Child(JSONSerializable, JSONDeserializable):

    def __init__(self):
        super().__init__()

        self.name = "child"
        self.bar = False
        self.children = []

    def get_child_object_types(self) -> Dict[str, Type[JSONSerializable]]:
        return {
            "children": GrandChild
        }


class GrandChild(JSONSerializable):

    def __init__(self):
        super().__init__()

        self.name = "grand child"
        self.age = 3
        self.something = 34.0


if __name__ == "__main__":

    root = Root()
    child = Child()
    child2 = Child()
    grand_child = GrandChild()

    root.children.append(child)
    root.children.append(child2)
    child.children.append(grand_child)
    root.grand_children.append(grand_child)

    json_string = root.serialize()
    print(json_string)  # JSON string

    parsed_dict = JSONInterpreter.parse_dict(json_string)
    parsed_root = JSONInterpreter.read(parsed_dict, Root())

    print(parsed_root.children[0].children[0].name)  # "grand child"
    print(parsed_root.children[0].name)  # "child"
    print(parsed_root.name)  # "root"
