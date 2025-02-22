import analysis
from stdlib import *


__temporary_names__: dict[str: analysis.RigInstruction] = {}


def rig_clear_function(the_string: str) -> str:
    """Special function for removing another symbols from object of string data."""

    res: str = ""

    for char in the_string:

        if char.isalnum():

            res += char
    else:

        return res


def main(path_to_file_with_code: str, *args: any, **kwargs: any) -> None:
    """
    The enter point of early Aurig interpreter.
    """

    f: list[analysis.RigToken] = analysis.rig_tokenization_proccess(path_to_file_with_code)
    f1: list[analysis.RigToken] = analysis.RigFormalGrammatic(f).rig_text_analys()
    f2: list[analysis.RigInstruction] = analysis.RigSemanticBuilder(f1, False).rig_markup_hub()

    python_code: str = """import stdlib\n\n"""
    
    for index, instruction in enumerate(f2):

        match instruction.operation:

            case instruction.operation if "create" in instruction.operation.content:

                if ":connection" in instruction.operation.content:
                    
                    __temporary_names__[F"[conn]{id(instruction)}"] = instruction
                    attribuits_of_conn: list[str] = [i[i.index('"') + 1: i.rindex('"')] for i in instruction.second_operand.content.split(" ; ")]
                    db_name: str = [__temporary_names__[key].first_operand.content for key in __temporary_names__ if "[db]" in key][0]
                    python_code += F"_{id(instruction)} = stdlib.RigConn('{instruction.result.content}', '_{id(instruction)}', '{db_name}', '{attribuits_of_conn[0]}', '{attribuits_of_conn[1]}', '{attribuits_of_conn[2]}')\n"
                    python_code += F"stdlib.rig_register_for_connections(_{id(instruction)})\n"
                elif ":table" in instruction.operation.content:
                    
                    __temporary_names__[F"[tab]{id(instruction)}"] = instruction
                    attribuits_of_table: list[str] = [i.replace(';', '').replace(' ', '') for i in instruction.second_operand.content.split(" ; ")]
                    db_name: str = [__temporary_names__[key].first_operand.content for key in __temporary_names__ if "[db]" in key][0]
                    attrs_string: str = str(list(attr for attr in attribuits_of_table)).replace("'", " ").replace("[", " ").replace("]", " ")
                    python_code += F"_{id(instruction)} = stdlib.RigTable('{instruction.result.content}', '_{id(instruction)}', '{db_name}', {attrs_string})\n"
                    python_code += F"stdlib.rig_register_for_tables(_{id(instruction)})\n"
                else:
                    
                    __temporary_names__[F"[db]{id(instruction)}"] = instruction
                    python_code += F"_{id(instruction)} = stdlib.RigDB('_{id(instruction)}', '{instruction.first_operand.content}')\n"
                
            case instruction.operation if "read" in instruction.operation.content:

                if instruction.result.content == instruction.second_operand.content:
                    
                    __temporary_names__[F"[bd_alias]{id(instruction)}"] = instruction
                    db_var_name: str =  "_" + str([key for key in __temporary_names__.keys() if __temporary_names__[key].first_operand.content == instruction.first_operand.content][0]).replace("[db]", "")
                    python_code += F"{db_var_name}.set_alias('{instruction.second_operand.content}')\n"
                elif instruction.result.content == "__buffer__":
                    
                    __temporary_names__[F"[buf]{id(instruction)}"] = instruction
                    db_var_name: str = str([key for key in __temporary_names__.keys() if "db" in key][0]).replace("[db]", "")
                    python_code += F"_{id(instruction)} = {db_var_name}.tables\n"
                else:
                    
                    __temporary_names__[F"[response]{id(instruction)}"] = instruction
                    selected_keys: list[str] = [
                        rig_clear_function(i) for index, i in enumerate([i for index, i in enumerate(instruction.first_operand.content.split()) if index % 2 == 0]) if index % 2 == 0
                        ]
                    selected_values: list[str] = [
                        rig_clear_function(i) for index, i in enumerate([i for index, i in enumerate(instruction.first_operand.content.split()) if index % 2 == 0]) if index % 2 != 0
                        ]
                    request_type_and_form_id: dict[str: str] = {key: value for key, value in zip(selected_keys, selected_values)}
                    python_code += F"_{id(instruction.result.content)} = stdlib.Response('{request_type_and_form_id['request']}', '{request_type_and_form_id['formid']}', {instruction.result.content})\n"
                    # python_code += F"_{id(instruction.result)} = rig_tables_objects_builder()"
                    # print(python_code)
                    # print([i for i in {key: __temporary_names__[key] for key in __temporary_names__}])
            case instruction.operation if "update" in instruction.operation.content:

                if ":append" in instruction.operation.content:

                    print(instruction.second_operand.content)
                elif ":set" in instruction.operation.content:

                    pass
                elif ":remove" in instruction.operation.content:

                    pass
            case instruction.operation if "delete" in instruction.operation.content:

                pass
            case instruction.operation if "insert" in instruction.operation.content:

                pass
            case instruction.operation if "condition" in instruction.operation.content:

                pass
    else:

        # print(python_code)
        pass


if __name__ == "__main__":

    main("field.aurig")
