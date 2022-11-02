
import ip_handler
import socket
import random

"""
Evan Hanes
Alan Garcia
19 october 2022
"""

def joinData(array) -> string:
    data = sorted(array, key=lambda key:array[0])
    string = ""
    for item in data:
        string += str(item[1], "ascii")
    return string



