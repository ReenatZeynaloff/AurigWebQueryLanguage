"""
18.11.2024.
"""

import socket
from typing import Sequence


__locals__: dict[str, list] = {}
__tables__: dict[str, list] = {}
__dynamic_tabless_objects__: dict[str, list] = {}
integer: str = "integer"
float_point: str = "float_point"
string: str = "string"
boolean: str = "boolean"


class RigDB(object):
    """The database type of Aurig."""

    name: str = ""
    var_name: str = ""
    alias: str = ""
    tables: list["RigTable"] = []
    connection: "RigConn" = None

    def __init__(self, var_name: str, name: str) -> None:
        """Initializator-method for create a new db file."""

        self.name = name
        super().__init__()
        self.var_name = var_name
        __locals__[self.name] = [self, self.var_name]

    def __repr__(self) -> str:
        """Representative method."""

        res: str = F"{self.name}: database(\n|\n|\n"

        if self.tables:
            
            sub_res: str = ' '.join(list(F"|---{self.tables[i]}\n" for i in range(len(self.tables))))
            temp_mid: list[str] = [elem for elem in sub_res.split("\n") if "\t" in elem]
            begin_ends: list[str] = [elem for elem in sub_res.split("\n") if "\t" not in elem]
            temp_mid = [elem.replace('\t', '|---|---') for elem in temp_mid]
            sub_res = begin_ends[0] + "\n" + ' '.join(list(F"{'' if index != 0 else ' '}{elem}\n" for index, elem in enumerate(temp_mid))) + "|---" + begin_ends[1]
            res += sub_res + "\n)"

        return res

    def set_alias(self, alias: str) -> None:
        """Method for set pseudo name for database."""

        self.alias = alias


class RigResponse(object):
    """The response type of Aurig."""

    method_type: str = ""
    form_id: str = ""
    data: list[any] = []

    def __init__(self, content_type: str, form_id: str, data: list[any]) -> None:
        """Initializator-method."""

        self.method_type = ["get" if content_type == "text/html" else "post"][0]
        self.form_id = form_id
        self.data = data
        super().__init__()

    def __repr__(self) -> str:
        """Method for text repsentation of object current Aurig's type."""

        ready_data: str = ' '.join([F'\n\t{i}' for i in self.data])
        res: str = F"\nREQUEST TYPE: {self.method_type}\nFROM FORM WITH: {self.form_id}\nHAS DATA:\t{ready_data}\nEND"

        return res


class RigTable(object):
    """The table type of Aurig."""

    table_name: str = ""
    var_name: str = ""
    alias: str = ""
    db_name: str = ""
    fields: dict[str: str] = {}
    count_of_amount_of_responses_objects: int = -1

    def __init__(self, table_name: str, var_name: str, db_name: str, **kwargs: dict[str, str]) -> None:
        """Initializator-method."""

        self.table_name = table_name
        self.var_name = var_name
        self.db_name = db_name
        self.fields = kwargs
        super().__init__()
        __locals__[self.table_name] = [self, var_name]
        self.db_var_name: str = __locals__[self.db_name][1]

    def __repr__(self) -> str:
        """Representative method."""

        res: str = F"{self.table_name}: table(\n"
        res += ''.join(list(F'\t{i}: {self.fields[i]},\n' for i in self.fields.keys()))
        res += ")"

        return res

    def counter_of_amount_of_responses_objects(self) -> None:
        """Special method for incrementation value of amount of respons's objects."""

        self.count_of_amount_of_responses_objects += 1

    def set_alias(self, alias: str) -> None:
        """Method for set pseudo name for database."""

        self.alias = alias

    def update(self, numbers_of_some_object: int | list[int, int] | tuple[int, int], operation_type: str = "set", **kwargs) -> None:
        """Update method."""

        get_our_table: str = [i for i in list(__dynamic_tabless_objects__.keys()) if i == self.table_name][0]

        if isinstance(numbers_of_some_object, Sequence):
            
            get_kwargss_keys: list[str] = list(kwargs.keys())
            diapasone_for_j_iterator: range = range(min(numbers_of_some_object), max(numbers_of_some_object))
            get_finding_objects: list[any] = [i for j in diapasone_for_j_iterator for i in __dynamic_tabless_objects__[get_our_table] if i.number == j]
            attributes_for_update: list[str] = [i for j in range(len(get_kwargss_keys)) for i in get_finding_objects[j].__annotations__.keys() if i == get_kwargss_keys[j]]
            
            if operation_type == "set":

                for get_finded_object in get_finding_objects:

                    for attribute_for_update in attributes_for_update:

                        get_finded_object.__annotations__[attribute_for_update] = kwargs[attribute_for_update]
            elif operation_type == "remove":

                for get_finded_object in get_finding_objects:

                    for attribute_for_update in attributes_for_update:

                        get_finded_object.__annotations__[attribute_for_update] = None
            elif operation_type == "append":

                for get_finded_object in get_finding_objects:

                    for attribute_for_update in attributes_for_update:

                        get_finded_object.__annotations__[attribute_for_update] += kwargs[attribute_for_update]
        else:

            get_kwargss_keys: list[str] = list(kwargs.keys())
            get_finding_object: any = [i for i in __dynamic_tabless_objects__[get_our_table] if i.number == numbers_of_some_object][0]
            attributes_for_update: list[str] = [i for j in range(len(get_kwargss_keys)) for i in get_finding_object.__annotations__.keys() if i == get_kwargss_keys[j]]
            
            if operation_type == "set":

                if len(kwargs) > 1:

                    for get_kwargss_key in get_kwargss_keys:
                        
                        for attribute_for_update in attributes_for_update:

                            if get_kwargss_key == attribute_for_update:

                                get_finding_object.__annotations__[attribute_for_update] = kwargs[get_kwargss_key]
                else:

                    get_finding_object.__annotations__[attributes_for_update[0]] = kwargs[get_kwargss_keys[0]]
            elif operation_type == "remove":

                if len(kwargs) > 1:

                    for get_kwargss_key in get_kwargss_keys:
                        
                        for attribute_for_update in attributes_for_update:

                            if get_kwargss_key == attribute_for_update:

                                get_finding_object.__annotations__[attribute_for_update] = None
                else:

                    get_finding_object.__annotations__[attributes_for_update[0]] = None
            elif operation_type == "append":

                if len(kwargs) > 1:

                    for get_kwargss_key in get_kwargss_keys:
                        
                        for attribute_for_update in attributes_for_update:

                            if get_kwargss_key == attribute_for_update:

                                get_finding_object.__annotations__[attribute_for_update] += kwargs[get_kwargss_key]
                else:

                    get_finding_object.__annotations__[attributes_for_update[0]] += kwargs[get_kwargss_keys[0]]

    def delete(self, numbers_of_some_object: int | list[int, int] | tuple[int, int], **kwargs) -> None:
        """Delete method."""

        get_our_table: str = [i for i in list(__dynamic_tabless_objects__.keys()) if i == self.table_name][0]

        if isinstance(numbers_of_some_object, Sequence):

            get_kwargss_values: list[str] = list(kwargs.values())
            diapasone_for_j_iterator: range = range(min(numbers_of_some_object), max(numbers_of_some_object))
            get_finding_objects: list[any] = [i for j in diapasone_for_j_iterator for i in __dynamic_tabless_objects__[get_our_table] if i.number == j]
            attributes_content_for_delete: str = [list(i.__annotations__.values()) for i in get_finding_objects]
            coincedences_amount: int = 0
            coincedences_objects: dict[any, int] = {}
            all_max_coinceded_objects: list[any] = []
      
            for index, i in enumerate(attributes_content_for_delete):
                
                for jindex, j in enumerate(i):
                    
                    if len(get_kwargss_values) > 1:

                        for k in get_kwargss_values:

                            if j == k:

                                coincedences_amount += 1
                                coincedences_objects[get_finding_objects[index]] = coincedences_amount
                    else:

                        if j == get_kwargss_values[0]:

                            coincedences_amount += 1
                            coincedences_objects[get_finding_objects[index]] = coincedences_amount
                else:

                    coincedences_amount = 0
            else:

                all_max_coinceded_objects = [i for i in coincedences_objects if coincedences_objects[i] == max(coincedences_objects.values())]

            for max_coinceded_object in all_max_coinceded_objects:

                __dynamic_tabless_objects__[get_our_table].remove(max_coinceded_object)
        else:
            
            __dynamic_tabless_objects__[get_our_table].pop(numbers_of_some_object)


def rig_tables_objects_builder(table_object: RigTable, responses_fields: RigResponse) -> any:
    """This function dedicated for creating the dynamic object's-type for concrete table object."""

    table_object.counter_of_amount_of_responses_objects()
    number_for_new_type: int = table_object.count_of_amount_of_responses_objects

    def __repr__(self: "new_type") -> str:
        """Function, which in further will have become the string representation method for dynamic class."""

        res: str = F"\nRESPONSES_PACKED_OBJECT_HAS: \n" + ' '.join([F'\t{i.capitalize()} = {self.__annotations__[i]}\n' for i in self.__annotations__.keys()])
        res += F"THIS PACKED_OBJECT UNDER NUMBER: \n\t(at {number_for_new_type} in '{table_object.table_name}' table)\n"

        return res

    def update_append(self: "new_type", attrs_name: any, some_value: any) -> None:
        """Function, which in further will have become the method for append some content in already ready object's attribute."""

        self.__annotations__[attrs_name] = self.__annotations__[attrs_name] + some_value

    def update_set(self: "new_type", attrs_name: any, some_value: any) -> None:
        """Function, which in further will have become the method for set some content in already ready object's attribute."""

        self.__annotations__[attrs_name] = some_value

    def update_remove(self: "new_type", attrs_name: any) -> None:
        """Function, which in further will have become the method for remove some content in already ready object's attribute."""

        self.__annotations__[attrs_name] = None

    new_type_name: str = F"response_type_{number_for_new_type}"
    new_type: type = type(new_type_name, (object, ), 
        {key: value for key, value in zip(table_object.fields, responses_fields.data)} | 
        {"__annotations__": {key: value for key, value in zip(table_object.fields, responses_fields.data)}} | 
        {"__repr__": __repr__, "update_append": update_append, "update_set": update_set, "update_remove": update_remove} | 
        {"number": table_object.count_of_amount_of_responses_objects})

    if table_object.table_name in __dynamic_tabless_objects__:

        __dynamic_tabless_objects__[table_object.table_name].append(new_type())
    else:

        __dynamic_tabless_objects__[table_object.table_name] = [new_type()]

    return new_type()


class RigConn(object):
    """The connection type of Aurig."""

    name: str = ""
    alias: str = ""
    db_name: str = ""
    protocol: str = ""
    host: str = ""
    port: int = 0
    all_content: list[RigResponse] = []
    __count_of_objects: int = 0

    def __init__(self, name: str, var_name: str, db_name: str, protocol: str, host: str, port: int) -> None:
        """Initializator-method."""

        self.name = name
        self.var_name = var_name
        
        if db_name in list(__locals__.keys()):

            self.db_name = db_name
        else:

            print(F"Database with name: '{db_name}', isn't exist!")
        
        if protocol.lower() in ["http", "https"]:
            
            self.protocol = protocol
        else:

            print(F"It isn't exist protocol with the: '{protocol}' name.")

        self.host = host
        self.port = int(port)
        super().__init__()
        do_continue: boolean | None = self.__inc_counting_of_selves()

        if do_continue:

            __locals__[self.name] = [self, self.var_name]
            self.db_var_name: str = __locals__[self.db_name][1]
            self.all_content = self.set_connection()

    def __repr__(self) -> str:
        """Representative method."""

        res: str = F"{self.name}: connection(\n\thost = {self.host},\n\tport = {self.port},\n\tprotocol = {self.protocol}\n)"

        return res

    @classmethod
    def __inc_counting_of_selves(cls) -> None | bool:
        """Special private class-method for increment."""

        if cls.__count_of_objects == 1:

            raise ConnectionError("Too many connection objects was created!")
        else:
            
            cls.__count_of_objects += 1
            return True

    def set_alias(self, alias: str) -> None:
        """Method for set pseudo name for database."""

        self.alias = alias

    def set_connection(self, path: str = "/") -> list[RigResponse]:
        """This method dedicated for do set the real connection with a some server."""

        GET_requester: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        GET_requester.connect((self.host, self.port))
        request: str = F"""GET {path} {self.protocol.upper()}/1.1\r\nHost: {self.host}\r\n\r\n"""
        GET_requester.sendall(request.encode("Utf-8"))
        GET_response: bytes = b""

        while True:

            chunk: bytes = GET_requester.recv(4096)
            answer_info: bytes = b"AUWQL_AGENT"
            GET_requester.send(answer_info)

            if not chunk:

                break
            else:
                
                GET_response += chunk

        GET_requester.close()
        
        count_of_responses_parts_without_body: int = len([i for i in GET_response.decode("Utf-8").split("\r\n\r\n", 1) if "<html>" not in i])
        responses_parts_with_forms_in_theyselves_body: list[str] = [i for i in GET_response.decode("Utf-8").split("\r\n\r\n", 1) if "<form" in i]

        res: list[RigResponse] = [
            RigResponse(
                [i for i in GET_response.decode("Utf-8").split("\r\n\r\n", 1)[0].split("\r") if "Content-Type" in i][0].split()[-1], 
                [i for i in [j for k in GET_response.decode("Utf-8").split("\r\n\r\n", 1)[1].split("\n") for j in k.split() if j != ' '] if "id" in i][0],
                [0, 1, 2, 3, 4, 5]
            ) for i in range(count_of_responses_parts_without_body) if responses_parts_with_forms_in_theyselves_body
        ]

        return res


def rig_register_for_connections(connection: RigConn) -> None:
    """This is special function for registration connection object to its attached database."""

    exec(F"{connection.db_var_name}.connection = {connection.var_name}")


def rig_register_for_tables(table_s: RigTable | Sequence[RigTable]) -> None:
    """This is special function for registration table or tables object(s) to their (its) attached database."""

    if isinstance(table_s, Sequence):

        exec(F"{table_s[0].db_var_name}.tables.extends({[F'{i.var_name}, ' for i in table_s]})")
    else:

        exec(F"{table_s.db_var_name}.tables.append({table_s.var_name})")


if __name__ == "__main__":

    my_database: RigDB = RigDB("my_database", "new_database")
    my_table: RigTable = RigTable("new_table", "my_table", "new_database", name="string", age="integer")
    my_second_table: RigTable = RigTable("new_table_of_orders", "my_second_table", "new_database", size="integer", valid="boolean")
    my_first_response: RigResponse = RigResponse("html/text", "0", ["Sarah", 24])
    my_second_response: RigResponse = RigResponse("html/text", "0", ["Yano", -15])
    my_third_response: RigResponse = RigResponse("html/text", "1", [180, 20])
    my_fourth_response: RigResponse = RigResponse("html/text", "0", ["Sarah", -15])
    rig_register_for_tables(my_table)
    rig_register_for_tables(my_second_table)
    my_1new_response_object: any = rig_tables_objects_builder(my_table, my_first_response)
    my_2new_response_object: any = rig_tables_objects_builder(my_table, my_second_response)
    my_3new_response_object: any = rig_tables_objects_builder(my_second_table, my_third_response)
    my_4new_response_object: any = rig_tables_objects_builder(my_table, my_fourth_response)
    # print([i for i in __dynamic_tabless_objects__["new_table"]])
    my_table.update([0, 3], name="Alex", age=17)
    print([i for i in __dynamic_tabless_objects__["new_table"]])
    # print(__dynamic_tabless_objects__)
    # my_connection: RigConn = RigConn("new_connection", "my_connection", "new_database", "HTTP", "localhost", 8000)
    # rig_register_for_connections(my_connection)
