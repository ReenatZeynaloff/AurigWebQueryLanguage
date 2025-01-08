import analysis
from stdlib import *


__temporary_names__: dict[str: analysis.RigInstruction] = {}


def main(path_to_file_with_code: str, *args: any, **kwargs: any) -> None:
    """
    Enter point.
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
                    python_code += F"_{id(instruction.result.content)} = stdlib.Response('post', {instruction.first_operand.content}, {instruction.result.content})\n"
            case instruction.operation if "update" in instruction.operation.content:

                pass
            case instruction.operation if "delete" in instruction.operation.content:

                pass
            case instruction.operation if "insert" in instruction.operation.content:

                pass
            case instruction.operation if "condition" in instruction.operation.content:

                pass
    else:

        print(python_code)


if __name__ == "__main__":

    main("field.aurig")
