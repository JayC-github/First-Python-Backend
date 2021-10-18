"""
############### Input_handling.py ################
A file for functions that are for input handling from the server.py
"""

from error import InputError


def input_handle_ids(input_str):
    """
    Input_handle_ids
    A function that takes in a string input version of an ID
    And output it's integer version.
    If the string is empty, return -1

    Input:
    - (str): input string
    Output:
    - (int): id converted from input string
    """

    if isinstance(input_str, int):
        return input_str

    if not isinstance(input_str, str):
        raise InputError(description="ERROR: INPUT invalid")

    if not input_str:
        return -1

    return int(input_str)
