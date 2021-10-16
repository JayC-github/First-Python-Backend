# pylint: disable=C0301
'''
############## storage.py ##################

A file for implementation of functions that we can use to pickle and unpickle a file for the backend server
'''


import pickle
import os.path

SERVER_DATA_STORAGE_PATH = "server_data.abc"

# Saves state of the server
def save_state(server_data):
    """
    Function that save the state of a server_data object

    Input:
    - (obj) the server data to save
    """
    with open(SERVER_DATA_STORAGE_PATH, 'wb') as file_in:
        pickle.dump(server_data, file_in)
        file_in.close()

def does_file_exist():
    """
    Function that checks if there is a file existed already

    Output:
    - (bool) check if the file exists
    """
    if os.path.isfile(SERVER_DATA_STORAGE_PATH):
        return True

    return False

def load_state():
    """
    Function that loads a state of the server_data

    Output:
    - (obj) the loaded object
    """
    if does_file_exist():
        return pickle.load(open(SERVER_DATA_STORAGE_PATH, 'rb'))

    return None
