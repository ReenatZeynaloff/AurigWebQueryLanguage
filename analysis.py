import datetime
from dataclasses import dataclass
from os import read
from pprint import pprint
from string import ascii_letters, digits
import re


symbols: list[str] = [
    "(", ")", "=", "*", ";", "<", ">", "<=>", "=="
]


special_words: list[str] = [
    "create", "read", 'update', "delete", "insert",
    "database", "table", "connection", "request", "response",
    "as", "in", "with", "not", "and", "or", "from", "for", "end",
    "integer", "float_point", "string", "boolean"
]


operations_names: list[str] = [
    "append", "remove", "set"
]


includes_idents: list[str] = [
    "protocol", "host", "port", "formid"
]


@dataclass
class RigToken(object):
    """Rig-token type."""

    content: str
    content_type: str
    list_index: int
    row_index: int


def rig_is_full_of_symbs(the_string) -> bool:
    """This function check, if string is fully containt only non-letter and non-digits symbol - return True."""

    res: bool = True

    for char in the_string:

        if char in [ascii_letters, digits]:

            res = False
    else:
        
        return res


def rig_string_clean(the_string: str) -> str:
    """Function for cleaning a some string from salvage like '= ( ) * ;' and etc."""
    
    res: str = ""

    if not rig_is_full_of_symbs(the_string):

        for char in the_string:

            if char not in symbols:

                res += char
        else:

            return res
    else:

        return the_string


def rig_typing(the_string: str) -> str:
    """Function for definition type of code bit as 'string'."""

    if the_string[0] in ["'", '"'] and the_string[-1] in ["'", '"']:

        return "string"
    elif "." in the_string and (the_string[0].isnumeric() or (the_string[0] == "-" and the_string[1].isnumeric())):
        
        return "float_point"
    elif the_string[0].isnumeric() or (the_string[0] == "-" and the_string[1].isnumeric()):

        return "integer"
    elif the_string.lower() in ["true", "false"]:

        return "boolean"
    elif the_string[0] == "(" and the_string[-1] == ")" and "<=>" in the_string:
        
        return "slice"
    elif the_string in operations_names:

        return "opname"
    elif the_string in symbols:

        if the_string == "(":

            return "begin_brace"
        if the_string == ")":

            return "end_brace"
        if the_string == "=":

            return "asignation"
        if the_string == ";":

            return "dotcomma"
    elif the_string in special_words:

        return "special_word"
    elif the_string in includes_idents:

        return "parameter"
    else:

        if the_string != "\u005c":
            
            return "identifier"


def rig_tokenization_proccess(path_to_subject: str) -> list[RigToken]:
    """Function, which do tokenizate on content of file with script. This proccess has been enumerating."""

    res: list[RigToken] = []
    subject: str = ""

    if path_to_subject.endswith(".aurig"):

        try:

            with open(path_to_subject, "r", encoding="Utf-8") as f:

                subject = f.read()
        except FileNotFoundError:

            print(f"The file on path: ({path_to_subject}) - didn't be find.")
    else:

        print("Why chosen your path to file isn't being correct?")
        return []
    for index_of_row, row in enumerate(subject.split("\n")):

        for index_of_subj, subj in enumerate(row.split()):
            
            elem: RigToken = RigToken(subj, rig_typing(rig_string_clean(subj)), index_of_subj, index_of_row + 1)
            res.append(elem)
        else:
            
            if len(row.split()) > 3 and row.split()[-1] != "\u005c":

                res.append(RigToken(R"\n", "nexting", index_of_subj, index_of_row + 1))
    else:
        
        return res


class RigInstruction(object):
    """This is realized data type from the node, which have more simplified structure."""

    operation: RigToken = None
    first_operand: RigToken = None
    second_operand: RigToken = None
    result: RigToken = None
    self_id: int = 64

    def __init__(self, operation: RigToken, first_operand: RigToken, second_operand: RigToken, result: RigToken) -> None:
        """Init. method."""

        self.operation = operation
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.result = result
        self.__private_id_incrementor()
        super().__init__()

    def __repr__(self) -> str:
        """Method for the text represantation of this class's object"""

        res: str = F"INSTRUCTION[{chr(self.self_id)}]:\n\t|--OPERATION: {self.operation.content}\n\t"
        res += F"|--FIRST_OPERAND: {(self.first_operand.content if self.first_operand is not None else '')}\n\t"
        res += F"|--SECOND_OPERAND: {(self.second_operand.content if self.second_operand is not None else '')}\n\t"
        res += F"|--RESULT: {self.result.content}\n"

        return res
    
    @classmethod
    def __private_id_incrementor(cls) -> None:
        """Especially method for incrementation value of 'self_id' for the type, after initialisation every new object of its."""

        cls.self_id += 1


class RigFormalGrammatic(object):
    """Type for describe our syntax laws and grammatic base."""

    line_array: list[RigToken] = []
    __temp_for_create_statement: list[RigToken] = []

    def __init__(self, list_of_rigotokes: list[RigToken]) -> None:
        """Init-method."""

        super().__init__()
        self.line_array = list_of_rigotokes

    def rig_read_micro_analys(self, some_row: list[RigToken]) -> bool:
        """Micro-analitical method for check a 'read'-expression."""
        
        res: bool = False
        some_row_content: str = ' '.join(tuple(i.content for i in some_row))

        match some_row:

            case some_row if len(some_row) < 2:

                print(F"Too much short syntax-sentence in your code!")
            case some_row if "read" != some_row[0].content:

                print(F"Why the 'read' word is absenting in first index in row: '{some_row_content}'?")
            case some_row if some_row[1].content_type != "identifier" and some_row[1].content not in ["request", "*"]:

                print(F"What is doing '{some_row[1].content}' at here '{some_row_content}'?")
            case some_row if some_row[1].content == "*" and some_row[2].content != "in":

                print(F"Where your 'in'-pretext in '{some_row_content}'?")
            case some_row if some_row[1].content == "*" and some_row[3].content_type != "identifier":

                print(F"Why at fourth index in '{some_row_content}' is absent a ident. name?")
                print(F"Remove this '{some_row[3].content_type}'-type value and will replace to exist callable name.")
            case some_row if "request" in list(i.content for i in some_row) and len(some_row) not in [10, 12]:

                print(F"Too much short syntax-sentence at row-index: {some_row[0].row_index}")
            case some_row if some_row[2].content == "as" and some_row[1].content_type != "identifier":

                print(F"You have error related with cause incorrect usage the pretext - 'as' in your syntax-sentence: '{some_row_content}'")
            case some_row if some_row[2].content != "as" and some_row[1].content not in ["request", "*"]:

                print(F"What are you want say that - '{' '.join([some_row[1].content, some_row[2].content])}' in sentence: '{some_row_content}'?")
                print("Please, be fix it, replace asignation to special word - 'as'")
            case some_row if len(some_row) == 4 and some_row[2].content == "as" and some_row[3].content_type != "identifier":
                
                print(F"After 'as' will should be placing a some identifier name, not a {some_row[3].content_type}!")
            case some_row if len(some_row) in [10, 12] and some_row[2].content_type == "asignation" and some_row[3].content_type != "string":

                print(F"Invalid value - '{some_row[3].content}' on {some_row[3].row_index}th row.")
            case some_row if len(some_row) > 4 and some_row[3].content_type == "identifier" and some_row[2].content in ["as", "in"]:

                print(F"Syntax error related with excess(es) element(s) in {some_row[3].row_index}th row - '{' '.join(tuple(i.content for i in some_row[4:]))}'.")
            case some_row if len(some_row) in [10, 12]:
                
                if some_row[4].content != "with":

                    print(F"Where your 'with' pretext in {some_row[4].row_index}th row?")
                if some_row[5].content != "formid":

                    print(F"Why instead of the 'formid' parameter you take '{some_row[5].content}'?")
                if some_row[6].content != "==":

                    print(F"Where your '==' symbol in {some_row[6].row_index}th row, between 'with' and '{some_row[7].content}'?")
                if some_row[7].content_type not in ["string", "integer"]:

                    print(F"Invalid value - '{some_row[3].content}' on {some_row[3].row_index}th row.")
                if some_row[8].content != "in" or some_row[9].content_type != "identifier":

                    print(F"You have been a syntax error in {some_row[9].row_index}th row!")
                if len(some_row) == 12 and (some_row[10].content != "as" or some_row[11].content_type != "identifier"):

                    print(F"You have been a syntax error in {some_row[11].row_index}th row!")
                else:

                    res = True
            case _:

                res = True
        return res

    def rig_create_micro_analys(self, some_row: list[RigToken], rows: list[list[RigToken]], the_res: list[RigToken]) -> bool:
        """Micro-analitical method for check a 'create'-expression."""
        
        res: bool = False
        some_row_content: str = ' '.join(tuple(i.content for i in some_row))

        class create_type:
            """The 'create'-type of one-namely special word."""
            
            announce_row: list[RigToken] = []
            body_rows: list[list[RigToken]] = []

            def __init__(self, announce_row: list[RigToken], body_rows: list[list[RigToken]]) -> None:
                """Init.-method."""
                
                self.announce_row = announce_row
                self.body_rows = body_rows

            def __str__(self) -> str:
                """For string image."""

                res: str = ' '.join(i.content for i in self.announce_row)

                for body_row in self.body_rows:

                    res += "\n" + ' '.join(i.content for i in body_row)
                else:
                    
                    return res

        match some_row:

            case some_row if some_row[0].content != "create":

                print(F"Why the 'create'-word not in first position in your sentence: '{some_row_content}'?")
            case some_row if len(some_row) == 4:

                if "identifier" not in [some_row[1].content_type, some_row_content[3]]:

                    if some_row[1].content_type != "identifier":

                        print(F"In {some_row[1].row_index}th sentences, you have an error related with first ident.-name!")
                    elif some_row[3].content_type != "identifier":

                        print(F"In {some_row[1].row_index}th sentences, you have an error related with second ident.-name!")
                elif some_row[2].content != "as":

                    print(F"Error related with this, that you haven't the 'as'-pretext in '{some_row_content}'.")
                else:

                    res = True
            case some_row if len(some_row) == 7:

                if some_row[1].content != "in":

                    print(F"In '{some_row_content}' exist error, that related with absence the 'in'-pretext.")
                elif some_row[2].content_type != "identifier":

                    print(F"In which DB are you want create a new table/connection")
                elif some_row[3].content not in ["table", "connection"]:

                    print(F"What the '{some_row[3].content}' in {some_row[3].row_index}th sentence? Did you mean 'table' or 'connection'?")
                elif some_row[4].content_type != "identifier":

                    print(F"And how are you want call this? Error was find in {some_row[4].row_index}th sentence.")
                elif some_row[5].content != "(" or some_row[6].content != "\u005c":

                    if some_row[5].content != "(":

                        print(F"You haven't a start braces in '{some_row_content}'!")
                    elif some_row[6].content != "\u005c" and not rows[rows.index(some_row) + 1][0].content:

                        print(F"Where in last position the sign of inverse-slash? Error was find in {some_row[6].row_index}th sentence.")
                
                indexs_sets: set[int] = set({})
                end_brace_index: int = 0

                for index, row in enumerate(rows):

                    if len(row) > 0 and row[0].content_type == "end_brace":
                        
                        if index > rows.index(some_row):

                            end_brace_index = index
                            break

                for index, row in enumerate(rows):
                    
                    if len(row) > 0 and (rows.index(some_row) < index < end_brace_index):

                        if row != some_row and row[-1].content == "\u005c" and row[-2].content_type != "begin_brace":

                            indexs_sets.add(index)
                else:
                    
                    indexs_sets = tuple(indexs_sets)
                    body_rows: list[list[RigToken]] = []

                    for index, row in enumerate(rows):

                        if index in indexs_sets:

                            body_rows.append(row)
                    else:
                        
                        create_object: create_type = create_type(some_row, body_rows)

                        for body_row in create_object.body_rows:

                            body_row_content: str = ' '.join(tuple(i.content for i in body_row))

                            match body_row:

                                case body_row if len(body_row) != 4:

                                    print(F"Lenght of line in your create-statement should be equals 4!")
                                    print(F"Error was detect in the {body_row[0].row_index}th sentence.")
                                    break
                                case body_row if body_row[0].content_type not in ["parameter", "identifier"]:

                                    print(F"Hey! In body by {some_row[3].content} of {some_row[4].content}, was find error!")
                                    print(F"Error is related with a insatisfactory name of first identifier: '{body_row_content}'")
                                    break
                                case body_row if body_row[1].content_type != "asignation":

                                    print(F"Where is an asign symbol (=) in the next sentence: '{body_row_content}'")
                                    break
                                case body_row if ((create_object.announce_row[3].content == "table" and body_row[2].content not in ["integer", "boolean", "string", "float_point"]) or \
                                    (create_object.announce_row[3].content == "connection" and body_row[2].content_type != "string")):
                                    
                                    print(F"Was detected an unknow or unsupported type of data - '{body_row[2].content_type}', in the next sentence: '{body_row_content}'")
                                    break
                                case body_row if body_row[3].content != "\u005c":

                                    print(F"You must ever to stand the backslash sign as last element of create-construction.")
                                    print(F"Error was detect in the next sentence: '{body_row_content}'")
                                    break
                                case _:

                                    res = True
                                    self.__temp_for_create_statement.extend(body_row)
            case some_row if len(some_row) not in [4, 7]:

                print(F"Your sentence's lenght in: '{some_row_content}', isn't a satisfactory value!")
            case _:

                res = True
        return res

    def rig_insert_micro_analys(self, some_row: list[RigToken]) -> bool:
        """Micro-analitical method for check an 'insert'-expression."""
        
        res: bool = False
        some_row_content: str = ' '.join(tuple(i.content for i in some_row))
        other_part_of_row: list[str] = list(i.content_type for i in some_row[5:len(some_row) - 1])

        match some_row:

            case some_row if len(some_row) < 5:
                
                print(F"Why lenght of row ({some_row_content}) small then five?")
            case some_row if "insert" != some_row[0].content or "in" != some_row[1].content:

                print(F"You have error related with announcement 'insert' or 'in' on this row: ({some_row_content})")
            case some_row if some_row[2].content_type != "identifier":

                print(F"Why third lexeme in ({some_row_content}) isn't a identifier?")
            case some_row if some_row[3].content != "response":

                print(F"Well, for what are you want to insert '{some_row[3].content}' for a place 'response'?")
            case some_row if len(some_row) == 5 and some_row[4].content_type != "identifier":

                print(F"You have error relative with problem, that last lexem - '{some_row[4]}', isn't a ident. name!")
            case some_row if (len(some_row) > 5 and some_row[4].content_type != "begin_brace" or some_row[-1].content_type != "end_brace" or \
                (other_part_of_row.count("identifier") > 1 and other_part_of_row.count("dotcomma") != other_part_of_row.count("identifier") - 1)):

                print(F"You have error on {some_row[0].row_index}th row's enumerate of elements!")
            case _:

                res = True
        return res

    def rig_update_micro_analys(self, some_row: list[RigToken]) -> bool:
        """Micro-analitical method for check an 'update'-expression."""
        
        res: bool = False
        some_row_content: str = ' '.join(tuple(i.content for i in some_row))

        match some_row:

            case some_row if some_row[0].content != "update":

                print(F"Why the 'update'-word not on first index in '{some_row_content}'?")
            case some_row if len(some_row) < 10:

                print(F"How so? Your: '{some_row_content}' - is too short!")
            case some_row if some_row[1].content_type not in ["integer", "slice"] and some_row[1].content != "*":

                print(F"The value of {some_row[1].content_type}-type isn't to support! This error had been find in '{some_row_content}'.")
            case some_row if some_row[2].content != "from":

                print(F"Where is a 'from'-word in {some_row[2].row_index}th sentence, after '{' '.join(tuple(i.content for i in some_row[0:2]))}'?")
            case some_row if some_row[3].content_type != "identifier":

                print(F"Why after 'from' in: '{some_row_content}' - isn't going a ident.-name?")
            case some_row if some_row[4].content != "in":

                print(F"Where the 'in'-pretext in '{some_row_content}'?")
            case some_row if some_row[5].content_type != "identifier":

                print(F"With which database you're working? Error in next sentence: '{some_row_content}'.")
            case some_row if some_row[6].content != "for":

                print(F"You haven't a 'for'-word in: '{some_row_content}'.")
            case some_row if some_row[7].content_type != "identifier":

                print(F"Where is a ident.-name in {some_row[7].row_index}th sentence?")
            case some_row if some_row[8].content_type != "opname":

                print(F"Why in your {some_row[8].row_index}th row don't present a 'append', 'remove' or 'set' words?")
            case some_row if some_row[9].content_type not in ["boolean", "integer", "float_point", "string", "identifier", "parameter"]:

                print(F"The {some_row[9].content_type}-type isn't a valid for next sentence: '{some_row_content}'.")
            case _:
                
                res = True
        return res

    def rig_delete_micro_analys(self, some_row: list[RigToken]) -> bool:
        """Micro-analitical method for check a 'delete'-expression."""
        
        res: bool = False

        match some_row:

            case some_row if "delete" != some_row[0].content:

                print(F"Why the 'delete'-word has not a firsten position in {some_row[0].row_index}th row?")
            case some_row if some_row[1].content_type not in ["slice", "integer"]:

                print(F"The {some_row[1].content_type}-type isn't supported for index to call!")
            case some_row if some_row[2].content != "from":
                
                print(F"Where the 'from'-word in '{some_row}'?")
            case some_row if some_row[3].content_type != "identifier":

                print(F"{some_row[3].content} isn't a to callable name!")
            case some_row if some_row[4].content != "in":

                print(F"What are you mean in {some_row[4].row_index}th sentence?")
            case some_row if some_row[5].content_type != "identifier":

                print(F"So, to whom you want to address? Error was detected in {some_row[5].row_index}th sentence.")
            case some_row if len(some_row) > 6:

                if some_row[6].content != "which" or some_row[7].content != "with":

                    print(F"Why are you thought, that from 6 to 7 indexes in {some_row[6].row_index}th sentence no need a true statement like 'which with'?")
                elif len(some_row) == 8:

                    print(F"Where a condition after 'which with' expression in {some_row[6].row_index}th row?")
                elif some_row[8].content_type != "identifier":

                    print(F"With what you are want to operating? Error was detected on {some_row[8].row_index}th row.")
                elif some_row[9].content not in ["<", "<=", "!=", "==", ">=", ">"]:
                    
                    print(F"How will to further do operating with data without operator in {some_row[9].row_index}th line?")
                elif some_row[10].content_type not in ["identifier", "slice", "integer", "boolean", "float_point", "string"]:

                    print(F"In the {some_row[10].row_index}th line it is existing a not accessable type's object!")
                else:

                    res = True
            case _:

                res = True
        return res

    def rig_condition_micro_analys(self, some_row: list[RigToken], rows: list[list[RigToken]]) -> bool:
        """Micro-analitical method for check a 'if'-statement."""

        res: bool = False
        some_row_content: str = ' '.join(tuple(i.content for i in some_row))
        next_row_content: str = ' '.join(tuple(i.content for i in rows[rows.index(some_row) + 1]))

        match some_row:
            
            case some_row if "if" not in some_row[0].content:

                print(F"What is doing 'if' at {some_row.index('if')}th index?")
            case some_row if len(some_row) < 3:

                print(F"Why your code-row '{some_row_content}' so short?")
            case some_row if ":" != some_row[-1].content:

                print(F"Where the ':'-symbol at last index on row: '{some_row_content}'?")
            case some_row if not next_row_content:

                print(F"Where is body of this condition: '{some_row_content}'?")
            case _:

                end_index: int = 0

                for index, row in enumerate(rows):
                    
                    row_content: tuple[str] = tuple(i.content for i in row)

                    if "end" in row_content and row[0].row_index > some_row[0].row_index:

                        end_index = index
                        break
                if end_index == 0:

                    print(F"Where the 'end'-word after body of condition statement?")
                    print(F"Error was finded at {some_row[0].row_index}th sentence!")
                else:

                    res = True
        return res

    def rig_text_analys(self) -> list[RigToken]:
        """This method dedicated for selection true positional tokens, based on my(our) syntax rules."""

        res: list[RigToken] = []
        sorted_line_array: list[RigToken] = sorted(self.line_array, key=lambda i: i.row_index, reverse=True)
        finally_row: int = sorted_line_array[0].row_index
        quad_array: list[list[RigToken]] = [[] for i in range(finally_row + 1)]
        i: int = 0
        i_row: int = 0

        for elem in self.line_array:
            
            if i_row != elem.row_index:
                
                i_row = elem.row_index
                i += 1
            if elem.content_type != "nexting":

                quad_array[i].append(elem)
        else:

            for row in quad_array:

                for word in row:

                    match word.content:
                        
                        case "read":

                            if self.rig_read_micro_analys(row):

                                res.extend(row)
                        case "create":

                            if self.rig_create_micro_analys(row, quad_array, res):

                                res.extend(row)
                                res.extend(self.__temp_for_create_statement)
                                self.__temp_for_create_statement = []
                        case "insert":

                            if self.rig_insert_micro_analys(row):

                                res.extend(row)
                        case "update":
                            
                            if self.rig_update_micro_analys(row):

                                res.extend(row)
                        case "delete":

                            if self.rig_delete_micro_analys(row):

                                res.extend(row)
                        case "if":
                        
                            if self.rig_condition_micro_analys(row, quad_array):
                                
                                res.extend(row)
            else:
                
                return res


class RigSemanticBuilder(object):
    """The semantic builder class for separate functionality from 'RigFormalGrammatic' and do construct special sem. markers for units."""

    flow_of_rig_tokens: list[RigToken] = []
    debuging: bool = None

    def __init__(self, flow_of_rig_tokens: list[RigToken], debuging: bool = True) -> None:
        """Init. method."""

        self.flow_of_rig_tokens = flow_of_rig_tokens
        self.debuging = debuging
        super().__init__()

    @staticmethod
    def rig_read_builder(rows_material: list[RigToken]) -> RigInstruction:
        """Method, which for build the instruction object above tokens of this (read) statement."""

        detected_root_operation: RigToken = rows_material[0]
        detected_first_operand: RigToken = None
        detected_second_operand: RigToken = None
        detected_result: RigToken = None
        pretext_index: int = 0

        for element in rows_material:

            if element.content == "as":

                pretext_index = element.list_index
        else:

            if pretext_index != 0:

                detected_result = (list(element for element in rows_material if element.list_index == pretext_index + 1) + [0])[0]
            else:

                detected_result = RigToken("__buffer__", "BUFF", None, None)

            if len(rows_material) == 4:

                if rows_material[2].content == "in":

                    detected_first_operand = rows_material[1]
                    detected_second_operand = rows_material[3]
                elif rows_material[2].content == "as":

                    detected_first_operand = rows_material[1]
                    detected_second_operand = rows_material[3]
            else:

                expressions: str = F"(({' '.join([i.content for i in rows_material[1: 4]])}) and ({' '.join([i.content for i in rows_material[5: 8]])}))"
                detected_first_operand = RigToken(expressions, "expressions", None, detected_root_operation.row_index)
                detected_second_operand = rows_material[pretext_index - 1]
                
            res: RigInstruction = RigInstruction(
                detected_root_operation,
                detected_first_operand,
                detected_second_operand,
                detected_result
            )

            return res

    @staticmethod
    def rig_update_builder(rows_material: list[RigToken]) -> RigInstruction:
        """Method, which for build the instruction object above tokens of this (update) statement."""

        detected_root_operation: RigToken = RigToken(F"update:{rows_material[-2].content}", "update", None, rows_material[0].row_index)
        detected_first_operand: RigToken = RigToken(
            F"{rows_material[5].content}.{rows_material[3].content}[{rows_material[1].content}].{rows_material[-3].content}", "expression", None, detected_root_operation.row_index
        )
        detected_second_operand: RigToken = RigToken(
            F"{rows_material[-1].content}", "object", None, detected_root_operation.row_index
        )
        detected_result: RigToken = RigToken(
            F"{rows_material[5].content}.{rows_material[3].content}", "table", None, detected_root_operation.row_index
        )
        res: RigInstruction = RigInstruction(
            detected_root_operation,
            detected_first_operand,
            detected_second_operand,
            detected_result
        )

        return res

    @staticmethod
    def rig_insert_builder(rows_material: list[RigToken]) -> RigInstruction:
        """Method, which for build the instruction object above tokens of this (insert) statement."""

        detected_root_operation: RigToken = rows_material[0]
        detected_first_operand: RigToken = rows_material[2]
        detected_second_operand: RigToken = None
        detected_result: RigToken = RigToken("__buffer__", "BUFF", None, None)
        array: str = ' '.join([i.content for i in rows_material[4:]])
        detected_second_operand = RigToken(array, "array", None, detected_root_operation.row_index)
        res: RigInstruction = RigInstruction(
            detected_root_operation,
            detected_first_operand,
            detected_second_operand,
            detected_result
        )

        return res

    @staticmethod
    def rig_delete_builder(rows_material: list[RigToken]) -> RigInstruction:
        """Method, which for build the instruction object above tokens of this (delete) statement."""

        detected_root_operation: RigToken = RigToken(
            F"delete:{rows_material[-2].content}", "delete", None, rows_material[0].row_index
        )
        slice_numbers: list[int, int] = []

        if "<=>" in rows_material[1].content:

            larger_index: int = rows_material[1].content.index("<")
            smaller_index: int = rows_material[1].content.index(">")
            slice_numbers.append(int(rows_material[1].content[1: larger_index]))
            slice_numbers.append(int(rows_material[1].content[smaller_index + 1: -1: 1]) + 1)
        detected_first_operand: RigToken = RigToken(
        F"{rows_material[5].content}.{rows_material[3].content}" +
        F"[{(rows_material[1].content if '<=>' not in rows_material[1].content else F'{slice_numbers[0]}:{slice_numbers[1]}')}]" + F".{rows_material[-3].content}", 
            "attribuits", None, detected_root_operation.row_index
        )
        detected_second_operand: RigToken = RigToken(
            F"{rows_material[-1].content}", "object", None, detected_root_operation.row_index
        )
        detected_result: RigToken = RigToken(
            F"{rows_material[5].content}.{rows_material[3].content}", "table", None, detected_root_operation.row_index
        )
        res: RigInstruction = RigInstruction(
            detected_root_operation,
            detected_first_operand,
            detected_second_operand,
            detected_result
        )

        return res

    @staticmethod
    def rig_create_builder(rows_material: list[RigToken], matrix: list[list[RigToken]]) -> RigInstruction:
        """Method, which for build the instruction object above tokens of this (create) construction."""

        detected_root_operation: RigToken = rows_material[0]
        detected_first_operand: RigToken = None
        detected_second_operand: RigToken = None
        detected_result: RigToken = None

        if len(rows_material) != 4:

            detected_root_operation = RigToken(
                F"create:{rows_material[3].content}", "create", None, rows_material[0].row_index
            )
            detected_first_operand = rows_material[2]
            current_index: int = matrix.index(rows_material)
            after_end_index: int = 0
            
            for index, row in enumerate(matrix[current_index + 1:]):

                row_content: str = ' '.join([i.content for i in row])

                if "\u005c" not in row_content:

                    after_end_index = index + current_index + 1
                    break
            body_rows_array: list[str] = [j.content for i in matrix[current_index + 1: after_end_index] for j in i]
            body_rows_string: str = ';'.join(' '.join(body_rows_array).split('\u005c'))

            detected_second_operand = RigToken(
                body_rows_string, 
                "table_body", None, None
            )
            detected_result = rows_material[4]
        else:

            detected_first_operand = rows_material[1]
            detected_result = rows_material[3]
        res: RigInstruction = RigInstruction(
            detected_root_operation,
            detected_first_operand,
            detected_second_operand,
            detected_result
        )

        return res

    @staticmethod
    def rig_if_builder(rows_material: list[RigToken]) -> RigInstruction:
        """Method, which for build the instruction object above tokens of this (if) construction."""

        detected_root_operation: RigToken = None
        detected_first_operand: RigToken = None
        detected_second_operand: RigToken = None

        def find_the_middle_operator() -> int:
            """The inner local function for find index of a middle operator in the 'if'-statement."""

            nonlocal rows_material
            res: RigToken = None
            operators: list[RigToken] = []

            for token in rows_material:

                if token.content in ["<", "<=", "!=", "==", ">=", ">", "and", "or", "not"]:

                    operators.append(token)
            else:

                middle_lenght: int = len(operators) // 2

                return rows_material.index(operators[middle_lenght])

        if len(rows_material) > 4:

            middle_operator_index: int = find_the_middle_operator()
            detected_root_operation = RigToken(
                F"condition:{rows_material[middle_operator_index].content}", "condition", None, rows_material[0].row_index
            )
            left_part: str = ' '.join([i.content for i in rows_material[1:middle_operator_index]])
            detected_first_operand = RigToken(
                left_part, "left_part", None, detected_root_operation.row_index
            )
            right_part: str = ' '.join([i.content for i in rows_material[middle_operator_index + 1: -1: 1]])
            detected_second_operand = RigToken(
                right_part, "right_part", None, detected_root_operation.row_index
            )
        elif len(rows_material) == 4 and rows_material[1].content == "not":

            detected_root_operation = RigToken("condition:negation", "condition", None, rows_material[0].row_index)
            detected_first_operand = rows_material[1]
            detected_second_operand = rows_material[2]
        elif len(rows_material) == 3:

            detected_root_operation = RigToken("condition:existing", "condition", None, rows_material[0].row_index)
            detected_first_operand = rows_material[1]
        detected_result: RigToken = RigToken("", "", None, None)
        res: RigInstruction = RigInstruction(
            detected_root_operation,
            detected_first_operand,
            detected_second_operand,
            detected_result
        )

        return res

    def rig_markup_hub(self) -> list[RigInstruction]:
        """The method, which is appear as central point of markuping the code part and give to them semantic matter."""

        res: list[RigInstruction] = []
        ready_array: list[RigToken] = list(sorted(self.flow_of_rig_tokens, key=lambda i: i.row_index))
        row_counter: int = len(list(i[1].row_index for i in list(filter( \
            lambda i: i[1].row_index if i[1].row_index != ready_array[i[0] - 1].row_index else 0, enumerate(ready_array)
        ))))
        ready_matrix: list[list[RigToken]] = [[] for i in range(row_counter)]
        matrixs_rows_index: int = 0

        for index, token in enumerate(self.flow_of_rig_tokens):

            try:

                future_token: RigToken = self.flow_of_rig_tokens[index + 1]
            except IndexError:

                future_token: RigToken = self.flow_of_rig_tokens[0]

            try:

                ready_matrix[matrixs_rows_index].append(token)
            except IndexError:

                pass

            if future_token.row_index != token.row_index:

                matrixs_rows_index += 1
        else:

            for ready_elem in ready_matrix:
                
                content_of_elem: str = ' '.join(tuple(i.content for i in ready_elem))

                if "read" in content_of_elem:

                    if self.debuging:

                        print(self.rig_read_builder(ready_elem))
                    else:
                        
                        res.append(self.rig_read_builder(ready_elem))
                elif "update" in content_of_elem:
                    
                    if self.debuging:

                        print(self.rig_update_builder(ready_elem))
                    else:
                        
                        res.append(self.rig_update_builder(ready_elem))
                elif "insert" in content_of_elem:
                    
                    if self.debuging:

                        print(self.rig_insert_builder(ready_elem))
                    else:
                        
                        res.append(self.rig_insert_builder(ready_elem))
                elif "delete" in content_of_elem:
                    
                    if self.debuging:

                        print(self.rig_delete_builder(ready_elem))
                    else:
                        
                        res.append(self.rig_delete_builder(ready_elem))
                elif "create" in content_of_elem:
                    
                    if self.debuging:

                        print(self.rig_create_builder(ready_elem, ready_matrix))
                    else:
                        
                        res.append(self.rig_create_builder(ready_elem, ready_matrix))
                elif "if" in content_of_elem:
                    
                    if self.debuging:

                        print(self.rig_if_builder(ready_elem))
                    else:
                        
                        res.append(self.rig_if_builder(ready_elem))
            else:
                
                return res


if __name__ == "__main__":

    grammatic_obj: RigFormalGrammatic = RigFormalGrammatic(rig_tokenization_proccess("field.aurig"))
    sema_obj: RigSemanticBuilder = RigSemanticBuilder(grammatic_obj.rig_text_analys())
    sema_obj.rig_markup_hub()

