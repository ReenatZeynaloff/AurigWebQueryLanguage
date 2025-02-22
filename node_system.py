from abc import abstractmethod, ABC
from pprint import pprint
from analysis import RigFormalGrammatic, RigToken, rig_tokenization_proccess


NODE: type = "MotherNode"


class MotherNode(ABC):
    """The abstract Node-like type in Aurig language."""
    
    name: str = ""
    token_obj_content: "RigToken" = None
    right_node: "MotherNode" = None
    central_node: "MotherNode" = None
    left_node: "MotherNode" = None
    is_root_node: bool = None
    __char_id_for_letter: int = 64

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
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
    def goto_right(self) -> any:
        """..."""

        pass

    @abstractmethod
    def goto_center(self) -> any:
        """..."""

        pass

    @abstractmethod
    def goto_left(self) -> any:
        """..."""

        pass


class CreateNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        pass
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


class ReadNode(MotherNode):
    """..."""

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        pass
    
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

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        pass
    
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

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        pass
    
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

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        pass
    
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

    def __init__(self, name: str, token_obj_content: "RigToken", right_node: "MotherNode", central_node: "MotherNode", left_node: "MotherNode", is_root_node: bool) -> None:
        """..."""
        
        super().__init__(name, token_obj_content, right_node, central_node, left_node, is_root_node)

    def __repr__(self) -> str:
        """..."""

        pass
    
    def goto_right(self) -> any:
        """..."""

        pass

    def goto_center(self) -> any:
        """..."""

        pass

    def goto_left(self) -> any:
        """..."""

        pass


__annotations_of_nodes_classes__: dict[str: list[type, str]] = {
    "CreateNode": [CreateNode, "create"],
    "ReadNode": [ReadNode, "read"],
    "UpdateNode": [UpdateNode, "update"],
    "DeleteNode": [DeleteNode, "delete"],
    "InsertNode": [InsertNode, "insert"],
    "ConditionNode": [ConditionNode, "if"],
}


def instructors_hub(tokens_expresion: list[list[RigToken]]) -> None:
    """..."""

    if len(tokens_expresion) > 1:

        for row in tokens_expresion:

            for token in row:

                pass

    else:

        tokens_expresion = tokens_expresion[0]

        for token in tokens_expresion:

            pass


def nodizer(token_flow: list[RigToken]) -> object:
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

                res: str = ""

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

                    pass
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
