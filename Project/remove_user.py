#pylint: disable=W0105
"""
################# remove_user.py ###################
A file for implementation of user removal from the server
"""

import constants as const
from error import AccessError
from verification import verify_user_id, verify_n_get_valid_token
'''
#Testing imports, can remove
from server_data_class import Server_data
from auth import auth_register
'''

def cleanup_channels(server_data, u_id):
    """
    A simple function that cleans the user off all channels

    Input:
    - (obj): the server data structure
    - (int): the user to be removed
    """
    for channel in server_data.get_channel_list():
        channel.remove_member(u_id)

def cleanup_sessions(server_data, u_id):
    """
    A simple function that deletes all that user's active tokens

    Input:
    - (obj): the server data structure
    - (int): the user to be removed
    """
    session = server_data.get_sessions_list()
    session.end_user_sessions(u_id)

def remove_user(server_data, token, u_id):
    """
    A function that validates the token, and removes the user from the server

    Input:
    - (str): token
    - ()
    """
    # Verification steps
    verify_user_id(server_data, u_id)
    u_id_admin = verify_n_get_valid_token(server_data, token)

    if u_id_admin == u_id:
        raise AccessError(description="The user can not remove itself")

    # Get admin user and check global permission
    admin_user = server_data.get_user_by_id(u_id_admin)
    if admin_user.global_permission_id != const.PERMISSION_GLOBAL_OWNER:
        raise AccessError(description="The user is not user of slackr")

    cleanup_channels(server_data, u_id)
    cleanup_sessions(server_data, u_id)

    # Perform action
    server_data.remove_user(u_id)
    return {}

'''
if __name__ == "__main__":
    server_data = Server_data()
    output1 = auth_register(server_data, "steven@gmail.com", "password", "c", "c")
    output2 = auth_register(server_data, "richard@gmail.com", "password2", "c", "c")
    output3 = auth_register(server_data, "nice@gmail.com", "password", "c", "c")
    output4 = auth_register(server_data, "try@gmail.com", "password", "c", "c")
    remove_user(server_data, output1["token"], output2["u_id"])
    print(server_data.pack_all_user_infos())
'''
