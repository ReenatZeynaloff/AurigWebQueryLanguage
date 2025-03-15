"""
Date of creating: 13.03.2025 .
"""

import typing
import sys
import io
from encoder import rig_Table_sample, rig_Table_example, BINS, __year__


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="Utf-8")
DEBINS: dict[int: str] = {
    "0000": 0,
    "0001": 1,
    "0010": 2,
    "0011": 3,
    "0100": 4,
    "0101": 5,
    "0110": 6,
    "0111": 7,
    "1000": 8,
    "1001": 9,
    "1010": "_"
}


def rig_decoding_process(file_path: str, debug: bool = False) -> typing.Sequence[rig_Table_example | rig_Table_sample]:
    """..."""

    the_result: typing.Sequence[rig_Table_example | rig_Table_sample] = []
    sub_result: str = ""
    file: io.TextIOWrapper = open(file_path, "r", encoding="Utf-8")
    sub_result = file.read()

    def debinning(binned_number: str) -> int:
        """..."""

        result: int = 0
        half_from_result: str = ""

        if BINS["_"] in binned_number:

            quads: list[list[str, str, str, str]] = [[] for i in range(4 + 1)]
            quads_index: int = 0
            quad: list[str] = []

            for index, digit in enumerate(binned_number):

                if index > 0 and index % 4 == 0:

                    quads_index += 1

                quads[quads_index].append(digit)
            else:
                
                for lst in quads:

                    quad.append(" ".join(lst).replace(" ", ""))
                else:
                    
                    quad = list(filter(lambda i: i if i != BINS["_"] else None, quad))
                    
                    for binned_num in quad:

                        half_from_result += str(DEBINS[binned_num])
                    else:
                        
                        half_from_result = int(half_from_result)
                        # print(chr(half_from_result - __year__))

        return result

    for word in sub_result.split():

        print(debinning(word))
    else:
        
        file.close()
        return the_result


if __name__ == "__main__":

    rig_decoding_process("my_database.axdb")
