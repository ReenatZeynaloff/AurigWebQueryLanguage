"""
Date of creating: 13.03.2025 .
"""

import time
import typing
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="Utf-8")
__year__: int = 0


BINS: dict[int: str] = {
    0: "0000",
    1: "0001",
    2: "0010",
    3: "0011",
    4: "0100",
    5: "0101",
    6: "0110",
    7: "0111",
    8: "1000",
    9: "1001",
    "_": "1010"
}


class rig_Table_sample(object):
    """..."""

    current_name: str = ""
    alias: str = ""
    fields: dict[str: str] = {}

    def __init__(self, current_name: str, alias: str, fields: dict[str: str]) -> None:
        """..."""

        self.current_name = current_name
        self.alias = alias
        self.fields = fields

    @staticmethod
    def repro__init__(representation: str) -> "rig_Table_sample":
        """..."""

        current_name: str = ""
        alias: str = ""
        fields: dict[str: str] = {}
        words_with_quad_braces: list[str] = []

        for row in representation.split("\n"):

            for word in row.split(" "):

                if "[" in word and "]" in word:

                    words_with_quad_braces.append(word)
        else:

            current_name = words_with_quad_braces[0][1:-1]
            alias = words_with_quad_braces[1][1:-1]
            fields = {key[1:-1]: value[1:-1] for key, value in zip(words_with_quad_braces[2::2], words_with_quad_braces[3::2])}
            result: "rig_Table_sample" = rig_Table_sample(current_name, alias, fields)

            return result

    def __repr__(self) -> str:
        """..."""

        result: str = F"TABLE_NAME: [{self.current_name}] WITH ALIAS: [{self.alias}]\n"
        result += " ".join([F"\t|FIELD_NAME: [{field}] \n\t|-> FIELD_VALUE: [{self.fields[field]}]\n" for field in self.fields])
        result += "-" * 50 + "\n" * 2

        return result


class rig_Table_example(object):
    """..."""

    current_ids_name: str = ""
    ids_alias: str = ""
    values: dict[str: str] = {}

    def __init__(self, current_ids_name: str, ids_alias: str, **values: dict[str: str]) -> None:
        """..."""

        self.current_ids_name = current_ids_name
        self.ids_alias = ids_alias
        self.values = values

        super().__init__()

    @staticmethod
    def repro__init__(representation: str) -> "rig_Table_sample":
        """..."""

        current_ids_name: str = ""
        ids_alias: str = ""
        values: dict[str: str] = {}
        words_with_quad_braces: list[str] = []

        for row in representation.split("\n"):

            for word in row.split(" "):

                if "[" in word and "]" in word:

                    words_with_quad_braces.append(word)
        else:

            current_ids_name = words_with_quad_braces[0][1:-1]
            ids_alias = words_with_quad_braces[1][1:-1]
            values = {key[1:-1]: value[1:-1] for key, value in zip(words_with_quad_braces[2::2], words_with_quad_braces[3::2])}
            result: "rig_Table_sample" = rig_Table_sample(current_ids_name, ids_alias, values)

            return result

    def __repr__(self) -> str:
        """..."""

        result: str = F"TABLE_NAME: [{self.current_ids_name}] WITH ALIAS: [{self.ids_alias}]\n"
        result += " ".join([F"\t|VALUE_NAME: [{value}] \n\t|-> VALUE_TYPE: [{self.values[value]}]\n" for value in self.values])
        result += "-" * 50 + "\n" * 2

        return result


def rig_encoding_process(database_name: str, indata: typing.Sequence[rig_Table_example | rig_Table_sample], debug: bool = False) -> None:
    """..."""

    __year__ = int(time.strftime("%Y"))
    age_coefficient: int = __year__ - 1996
    sub_result: list[int] = []
    result: str = ""

    def binning(number: int) -> str:
        """..."""

        result: str = ""

        if number < 10:

            result = BINS[number]
        else:

            result = BINS["_"] + " ".join([BINS[int(i)] for i in str(number)]).replace(" ", "") + BINS["_"]

        return result
    
    [sub_result.extend(i) for i in list(map(lambda i: [binning(ord(j) + age_coefficient) for j in str(i)], indata))]

    for index, i in enumerate(sub_result):

        result += i + " "

        if index % 4 == 0:

            result += "\n"
    else:

        if debug:

            print(result)

        with open(F"{database_name}.axdb", "w", encoding="Utf-8") as file:

            file.write(result)



if __name__ == "__main__":

    t1: rig_Table_sample = rig_Table_sample("users", "", {"login": "string", "password": "string", "age": "integer"})
    t2: rig_Table_sample = rig_Table_sample("orders", "", {"title": "string", "price": "float", "producted_date": "datetime"})
    rig_encoding_process("my_database", [t1, t2], False)
