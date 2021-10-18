"""
################# channels.py ####################
A file for the channels related functions for the backend server

Using resources from:
server_data_class
channel_class
session_class
user_class
error

Contains functions:
channels_list
channels_listall
channels_create
"""
# pylint: disable=W0105, C0301

from error import AccessError, InputError
from verification import verify_n_get_valid_token


def channels_create(server_data, token, name, is_public):

    """
    channel_create function:
    A function that creates a channel in the server_data, if the token is valid. Returns a channel_id from the server_data function

    Inputs:
    - server_data (obj)
    - token (string)
    - name (string)
    - is_public (bool)

    Outputs
    - {channel_id} (dics)
    """

    # Check if the token is active, and get u_id if the token is active
    # Get u_id from the active session
    u_id = verify_n_get_valid_token(server_data, token)

    # Get user object from the u_id
    user_obj = server_data.get_user_by_id(u_id)
    # Then get the user info containing {u_id, name_first, name_last}
    user_info = user_obj.get_user_member_info()

    # Now check if the name is longer than 20 characters
    if len(name) > 20:
        raise InputError(description="Channel name too long")

    # Everything checks out, create channel in the database
    channel_id = server_data.create_channel(name, user_info, is_public)

    return {"channel_id": channel_id}


def channels_listall(server_data, token):
    """
    channels_listall function:
    A function that lists all channels and their details with a valid token

    Input:
    - token (string)

    Output:
    - {channels} (dic of list of {channel_id, name})
    """


    # Check if the token is active
    u_id = verify_n_get_valid_token(server_data, token)
    rt_list = server_data.pack_all_channel_infos()
    return rt_list


def channels_list(server_data, token):
    """
    channels_list function:
    A function that lists all channels and their details with a valid token that a user is a part of

    Input:
    - token (string)

    Output:
    - {channels} (dic of list of {channel_id, name})
    """


    # Check if the token is active
    # If active, get the u_id from this token and perform action required
    u_id = verify_n_get_valid_token(server_data, token)
    rt_list = server_data.pack_channels_info_by_user(u_id)

    return rt_list

'''
if __name__ == "__main__":
    server_data = Server_data()
    u_id = server_data.new_user("richard@gmail.com", "12345", "Richard", "Park", "richardpark", 1)
    token = "ABCDE"

    sessions = server_data.get_sessions_list()
    sessions.create_active_session(u_id, token)

    channel_id1 = channels_create(server_data, token, "TEST1", True)
    channel_id2 = channels_create(server_data, token, "TEST2", True)
    print (channel_id1)
    print (channel_id2)

    print (channels_listall(server_data, token))
    print (channels_list(server_data, token))

    u_id2 = server_data.new_user("steven@gmail.com", "12345", "Steven", "Yang", "stevenyang", 1)
    token2 = "CDEFG"
    sessions.create_active_session(u_id2, token2)

    print (channels_listall(server_data, token2))
    print (channels_list(server_data, token2))

    token = "A"
    print (channels_list(server_data, token))
        
'''