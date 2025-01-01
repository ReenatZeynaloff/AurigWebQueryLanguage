"""
18.11.2024.
"""

import socket
from typing import Sequence


__locals__: dict[str: list] = {}
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


class RigTable(object):
    """The table type of Aurig."""

    table_name: str = ""
    var_name: str = ""
    alias: str = ""
    db_name: str = ""
    fields: dict[str: str] = {}

    def __init__(self, table_name: str, var_name: str, db_name: str, **kwargs: dict[str: str]) -> None:
        """Initializator-method."""

        self.table_name = table_name
        self.var_name = var_name
        self.db_name = db_name
        self.fields = kwargs
        super().__init__()
        __locals__[self.table_name] = [self, var_name]
        self.db_var_name: str = __locals__[self.db_name][1]

    def __repr__(self) -> str:
        """Representtive method."""

        res: str = F"{self.table_name}: table(\n"
        res += ''.join(list(F'\t{i}: {self.fields[i]},\n' for i in self.fields.keys()))
        res += ")"

        return res

    def set_alias(self, alias: str) -> None:
        """Method for set pseudo name for database."""

        self.alias = alias

    def update(self) -> None:
        """Update method."""

        pass

    def delete(self) -> None:
        """Delete method."""

        pass


class RigResponse(object):
    """The response type of Aurig."""

    method_type: str = ""
    form_id: str = ""

    def __init__(self, content_type: str, form_id: str) -> None:
        """Initializator-method."""

        self.method_type = ["get" if content_type == "text/html" else "post"][0]
        self.form_id = form_id
        super().__init__()


class RigConn(object):
    """The connection type of Aurig."""

    name: str = ""
    alias: str = ""
    db_name: str = ""
    protocol: str = ""
    host: str = ""
    port: int = 0
    all_content: list[RigResponse] = []

    def __init__(self, name: str, var_name: str, db_name: str, protocol: str, host: str, port: int) -> None:
        """Initializator-method."""

        self.name = name
        self.var_name = var_name
        
        if db_name in list(__locals__.keys()):

            self.db_name = db_name
        else:

            print(F"Database with name: '{db_name}',' isn't exist!")
        
        if protocol.lower() in ["http", "https"]:
            
            self.protocol = protocol
        else:

            print(F"It isn't exist protocol with the: '{protocol}' name.")

        self.host = host
        self.port = int(port)
        super().__init__()
        __locals__[self.name] = [self, self.var_name]
        self.db_var_name: str = __locals__[self.db_name][1]
        self.all_content = self.__set_connection()

    def __repr__(self) -> str:
        """Representative method."""

        res: str = F"{self.name}: connection(\n\thost = {self.host},\n\tport = {self.port},\n\tprotocol = {self.protocol}\n)"

        return res

    def set_alias(self, alias: str) -> None:
        """Method for set pseudo name for database."""

        self.alias = alias

    def __set_connection(self) -> list[RigResponse]:
        """This private method dedicated for do set the real connection with a some server."""

        client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        request: str = F"""POST / {self.protocol.upper()}/1.1\r\nHost: {self.host}\r\n\r\n"""
        client.sendall(request.encode("Utf-8"))
        response: bytes = b""

        while True:

            chunk: bytes = client.recv(4096)

            if not chunk:

                break
            else:
                
                response += chunk

        client.close()
        
        print([i for i in response.decode("Utf-8").split("\r\n\r\n", 1)[0].split("\r") if "Content-Type" in i][0].split()[-1])
        # res: list[RigResponse] = [
        #     RigResponse(
        #         [i for i in response.decode("Utf-8").split("\r\n\r\n", 1)[0].split("\r") if "Content-Type" in i][0].split()[-1]
        #     ) for i in response.decode("Utf-8").split("\r\n\r\n", 1)]
        # return res


def register_for_connections(connection: RigConn) -> None:
    """This is special function for registration connection object to its attached database."""

    exec(F"{connection.db_var_name}.connection = {connection.var_name}")


def register_for_tables(table_s: RigTable | Sequence[RigTable]) -> None:
    """This is special function for registration table or tables object(s) to their (its) attached database."""

    if isinstance(table_s, Sequence):

        exec(F"{table_s[0].db_var_name}.tables.extends({[F'{i.var_name}, ' for i in table_s]})")
    else:

        exec(F"{table_s.db_var_name}.tables.append({table_s.var_name})")


if __name__ == "__main__":
    # 
    db1: RigDB = RigDB("db1", "first_db")
    conn1: RigConn = RigConn("first_conn", "conn1", "first_db", "HTTP", "localhost", 8000)
    # tablo1: RigTable = RigTable("users", "tablo1", "first_db", name="str", age="int", adult="bool")
    register_for_connections(conn1)
    # register_for_tables(tablo1)
