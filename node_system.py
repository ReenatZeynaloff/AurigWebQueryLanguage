"""
Data, when this module was formed: 29.01.2025 .
"""

from abc import abstractmethod, ABC
from pprint import pprint
from analysis import RigFormalGrammatic, RigToken, rig_tokenization_proccess

NODE: type = "MotherNode"
_TREE: type = dict[NODE, list[NODE]]
__trees__: list[_TREE] = []


class MotherNode(ABC):
    """The abstract Node-like type in Aurig language."""
    
    name: str = ""
    token_obj_content: "RigToken" = None
    right_node: "MotherNode" = None
    central_node: "MotherNode" = None
    left_node: "MotherNode" = None
    is_root_node: bool = None
    __char_id_for_letter: int = 64

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""

        self.name = name
        self.token_obj_content = token_obj_content
        self.right_node = right_node
        self.central_node = central_node
        self.left_node = left_node 
        self.is_root_node = is_root_node

        super().__init__()

    @abstractmethod
    def __repr__(self) -> str:
        """..."""

        pass
    
    @abstractmethod
    def goto_right(self) -> "MotherNode":
        """..."""

        pass

    @abstractmethod
    def goto_center(self) -> "MotherNode":
        """..."""

        pass

    @abstractmethod
    def goto_left(self) -> "MotherNode":
        """..."""

        pass


class CreateNode(MotherNode):
    """..."""

    is_root_node: bool = None

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        result: str = ""

        return result
    
    def goto_right(self) -> MotherNode:
        """..."""

        pass

    def goto_center(self) -> MotherNode:
        """..."""

        pass

    def goto_left(self) -> MotherNode:
        """..."""

        pass


class ReadNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        result: str = ""

        return result
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


class UpdateNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        result: str = ""

        return result
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


class DeleteNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        result: str = ""

        return result
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


class InsertNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        result: str = ""

        return result
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


class ConditionNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", 
    right_node: "MotherNode" = None, central_node: "MotherNode" = None, left_node: "MotherNode" = None, is_root_node: bool = False) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        result: str = ""

        return result
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


__annotations_of_nodes_classes__: (ANNOTTYPE:=dict[str, list[type, str]]) = {
    "CreateNode": [CreateNode, "create"],
    "ReadNode": [ReadNode, "read"],
    "UpdateNode": [UpdateNode, "update"],
    "DeleteNode": [DeleteNode, "delete"],
    "InsertNode": [InsertNode, "insert"],
    "ConditionNode": [ConditionNode, "if"],
}


def create_tree_builder(creates_expression: list[RigToken], create_body: list[list[RigToken]], rows_matrix: list[list[RigToken]]) -> bool:
    """..."""

    result: bool = False
    general_creates_rows: list[list[RigToken]] = create_body + creates_expression

    if len(create_body) > 1:

        root_node: CreateNode = CreateNode("init", creates_expression[0], 
        right_node=CreateNode("place", creates_expression[1], right_node=CreateNode("obj:name", creates_expression[2])), 
        left_node=CreateNode("type", creates_expression[3], right_node=CreateNode("obj:name", creates_expression[4])),
        central_node=CreateNode(""))
    else:

        __trees__.append({})

        if len(creates_expression) == 2:

            root_node: CreateNode = CreateNode("init", creates_expression[0], right_node=CreateNode("obj:name", creates_expression[1]), is_root_node=True)
            __trees__[-1][root_node] = [root_node.right_node, root_node.left_node, root_node.left_node.right_node]
        else:

            root_node: CreateNode = CreateNode("init", creates_expression[0], 
            right_node=CreateNode("obj:name", creates_expression[1]), left_node=CreateNode("alias", creates_expression[2], CreateNode("obj:alias", creates_expression[3])), 
            is_root_node=True)
            __trees__[-1][root_node] = [root_node.right_node, root_node.left_node, root_node.left_node.right_node]

    return result


def get_create_bodys_rows(creates_expression: list[RigToken], rows_matrix: list[list[RigToken]]) -> dict[bool, list[list[RigToken]]]:
    """Special function, which return the dictionary with key about having of body and value of self body."""

    sub_result: list[list[RigToken]] = []
    index_of_current_expression: int = rows_matrix.index(creates_expression)
    it_has_body: bool = False
    rows_with_body: list[list[RigToken]] = []
    creators_counter: dict[int, str] = {}
    existing_of_withoutbodylike_creates: bool = False
    result: dict[bool, list[list[RigToken]]] = {}

    for row in rows_matrix[index_of_current_expression:]:
        
        if row[0].content == __annotations_of_nodes_classes__["CreateNode"][1]:

            creators_counter[row[0].row_index] = " ".join([i.content for i in row])

            if row[-2].content_type == "begin_brace":

                it_has_body = True
            else:
                
                it_has_body = False
                existing_of_withoutbodylike_creates = True

            if it_has_body:

                rows_with_body.append(row)
                
                for key in list(creators_counter.keys()):

                    if "(" not in creators_counter[key]:

                        creators_counter.pop(key)
                else:
                    
                    if len(creators_counter) == 1:

                        if not existing_of_withoutbodylike_creates:

                            for index, current_row in enumerate(rows_matrix[index_of_current_expression + 1:]):

                                future_row: list[RigToken] = rows_matrix[index_of_current_expression + 1:][index + 1]

                                sub_result.append(current_row)

                                if future_row[-1].content_type != "slash" or future_row[0].content == __annotations_of_nodes_classes__["CreateNode"][-1]:

                                    break
    else:

        if not existing_of_withoutbodylike_creates:

            result = {it_has_body: sub_result}
        else:

            result = {not it_has_body: sub_result}

        return result


def nodizer(token_flow: list[RigToken]) -> None:
    """The large function ..."""

    result: list[dict[NODE: list[NODE]]] = []
    amount_of_rows: int = len(list(filter(lambda i: i[1] != [i.row_index for i in token_flow][i[0] - 1], enumerate([i.row_index for i in token_flow]))))
    really_rows: list[list] = [[] for i in range(len(token_flow))]
    current_token_list: list[RigToken] = []

    for index, token in enumerate(token_flow):

        try:

            future_token: RigToken = token_flow[index + 1]
        except IndexError:

            future_token: RigToken = token_flow[0]
        finally:
        
            if token.row_index == future_token.row_index:

                current_token_list.append(token)
            else:

                current_token_list.append(token)

                for current_token in current_token_list:

                    really_rows[index].append(current_token)
                else:
                    
                    current_token_list = []
    else:

        really_rows = list(filter(lambda i: i if i != [] else 0, really_rows))

        class NodizedCluster(object):
            """Aurig's class for pack a row in 'really_rows' in more plastic wrapper."""

            row_of_tokens: list[RigToken] = []
            rows_len: int = 0
            first_token: RigToken = None
            last_token: RigToken = None

            def __init__(self, row_of_tokens: list[RigToken]) -> None:
                """..."""

                self.row_of_tokens = row_of_tokens
                self.rows_len = len(row_of_tokens)
                self.first_token = row_of_tokens[0]
                self.last_token = row_of_tokens[-1]

                super().__init__()

            def __repr__(self) -> str:
                """..."""

                result: str = ""

                return super().__repr__()

        for cluster in [NodizedCluster(i) for i in really_rows]:

            cluster_content: str = " ".join([i.content for i in cluster.row_of_tokens])

            for name_of_node_class in __annotations_of_nodes_classes__:

                its_ok: bool = False
                current_cluster_is_root: bool = False
                get_center_for_current_cluster: NodizedCluster = None
                get_left_cluster_for_current: NodizedCluster = None
                get_right_cluster_for_current: NodizedCluster = None

                if ((cluster_content.split()[0] == __annotations_of_nodes_classes__[name_of_node_class][-1]) and \
                (name_of_node_class == list(__annotations_of_nodes_classes__.keys())[0])):
                    
                    creates_dict: dict[bool: list[list[RigToken]]] = get_create_bodys_rows(cluster.row_of_tokens, really_rows)
                    its_ok = create_tree_builder(cluster.row_of_tokens, creates_dict[list(creates_dict.keys())[-1]], really_rows)
                elif ((cluster_content.split()[0] == __annotations_of_nodes_classes__[name_of_node_class][-1]) and \
                (name_of_node_class == list(__annotations_of_nodes_classes__.keys())[1])):

                    pass
                elif ((cluster_content.split()[0] == __annotations_of_nodes_classes__[name_of_node_class][-1]) and \
                (name_of_node_class == list(__annotations_of_nodes_classes__.keys())[2])):

                    pass
                elif ((cluster_content.split()[0] == __annotations_of_nodes_classes__[name_of_node_class][-1]) and \
                (name_of_node_class == list(__annotations_of_nodes_classes__.keys())[3])):

                    pass
                elif ((cluster_content.split()[0] == __annotations_of_nodes_classes__[name_of_node_class][-1]) and \
                (name_of_node_class == list(__annotations_of_nodes_classes__.keys())[4])):

                    pass
                elif ((cluster_content.split()[0] == __annotations_of_nodes_classes__[name_of_node_class][-1]) and \
                (name_of_node_class == list(__annotations_of_nodes_classes__.keys())[5])):

                    pass

                if its_ok:

                    __annotations_of_nodes_classes__[name_of_node_class][0](
                        str(id(cluster)), cluster.first_token, get_right_cluster_for_current, get_center_for_current_cluster, get_left_cluster_for_current, current_cluster_is_root
                        )
        else:

            return result


if __name__ == "__main__":

    gramma_object: RigFormalGrammatic = RigFormalGrammatic(rig_tokenization_proccess("field.aurig"))
    nodized_object: object = nodizer(gramma_object.rig_text_analys())
