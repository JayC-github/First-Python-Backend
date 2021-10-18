#pylint: disable=C0301
"""
############# Verification.py ################
A file for functions that verifies inputs such as valid token, valid channel, valid messages etc so it can be reused across channels
"""

import constants as const
from error import InputError, AccessError

def verify_n_get_valid_token(server_data, token):
    """
    A function that checks if a token is valid
    Returns the u_id if the token is valid, raise error if not

    Use this to check:
    If the token is valid
    Get the u_id from the an active token

    Input:
    - (obj) the server_data
    - (str) the token to check if its valid
    Output:
    - (Error) if the token is incorrect or invalid
    - (int) u_id if the tken is valid
    """
    if not isinstance(token, str):
        raise InputError(description="token is not in the correct format")

    session_obj = server_data.get_sessions_list()
    if not session_obj.is_token_active(token):
        raise AccessError(description="Invalid token")

    return session_obj.get_token_user(token)

def verify_user_id(server_data, u_id):
    """
    A function that verifies the input user_id
    Raise error if the user does not exist

    Use this to check:
    If the user with u_id exists

    Input:
    - (obj) server_data object
    - (int) the u_id of the user to verify
    """
    if not isinstance(u_id, int):
        raise InputError(description="u_id is not in the correct format")

    if not server_data.does_user_exist(u_id):
        raise InputError(description="Invalid User")

def verify_channel_id(server_data, channel_id):
    """
    A function that verifies the input channel_id
    Raise error if the channel does not exist

    Use this to check:
    If the channel_ID exists

    Input:
    - (obj) server_data object
    - (int) the channel_id of the channel to verify
    """
    if not isinstance(channel_id, int):
        raise InputError(description="channel_id is not in the correct format")

    if not server_data.does_channel_exist(channel_id):
        raise InputError(description="Invalid channel ID")

def verify_message_id(server_data, message_id, u_id):
    """
    A function that verifies the input message_id
    Raise error if the message_id does not exist in the server data,
    or if the message exist it does not belong to a channel that the user have
    access to
    Use this to check:
    If the message_id exists
    If the message belongs to a channel that the user has access to

    Input:
    - (obj) server_data object
    - (int) the message_id of the message to verify
    - (int) the u_id of the user to verify
    """
    if not isinstance(message_id, int):
        raise InputError(description="message_id is not in the correct format")

    channel_id = server_data.find_channel_by_message_id(message_id)
    if channel_id == -1:
        raise InputError(description="Invalid message_id")

    channel_obj = server_data.get_channel_by_id(channel_id)
    if not channel_obj.is_user_member(u_id):
        raise InputError(description="User does not have access to the channel the message is in")

def verify_react_id(server_data, react_id):
    """
    A simple function that verifies if a react_id exists in the server
    Use this to check:
    If react ID exists in server

    Input:
    - (obj) server_data object
    - (int) the react_id of the reaction to verify
    """
    if react_id != const.REACT_THUMBS_UP_ID:
        raise InputError(description="Invalid react id")

def verify_react_id_in_message(server_data, message_id, react_id):
    """
    A function that verifies if a react_id exists in a message
    Use this to check:
    If message contains such react_id

    Input:
    - (obj) server_data object
    - (int) the message_id of the message to verify
    - (int) the react_id of the react in message
    """
    verify_react_id(server_data, message_id)

    message_obj = server_data.find_message_by_message_id(message_id)
    if message_obj is None:
        raise InputError(description="ERROR: MESSAGE OBJECT NOT FOUND")

    if not message_obj.does_reaction_type_exist(react_id):
        raise InputError(description=f"message with ID {message_id} does not contain an active React with React ID {react_id}")

# Access Verifications
def verify_user_channel_status(server_data, channel_id, u_id, needed_permission):
    """
    A function that checks if a user is authorized in a particular channel
    The particular permission needed is specified in needed_permission
    Use this to check:
    If a user is a member of the channel/owner of slackr
    If a user is a owner of the channel/owner of slackr

    Input:
    - (obj) server_data object
    - (int) the channel_id of the channel to verify
    - (int) the u_id of the user to verify
    - (int) the permission it is looking for
    """
    if not isinstance(channel_id, int):
        raise InputError(description="channel_id is not in the correct format")

    if not isinstance(u_id, int):
        raise InputError(description="u_id is not in the correct format")

    channel_obj = server_data.get_channel_by_id(channel_id)
    user_obj = server_data.get_user_by_id(u_id)
    # If user is owner of slackr, the user has all permissions
    if user_obj.global_permission_id != const.PERMISSION_GLOBAL_OWNER:
        if needed_permission == const.PERMISSION_LOCAL_OWNER:
            if not channel_obj.is_user_owner(u_id):
                raise AccessError(description="User does not have permission as owner OR owner of slackr")

        elif needed_permission == const.PERMISSION_LOCAL_MEMBER:
            if not channel_obj.is_user_member(u_id):
                raise AccessError(description="User does not have permission as member")
        else:
            raise InputError(description="ERROR: Unexpected permission input")

def verify_user_channel_access(server_data, channel_id, u_id, status_required):
    """
    A function that verifies if a user is in channels or not, depending on the status.
    Use this to check:
    If a user is in the channel
    If a user is NOT in the channel

    Input:
    - (obj) server_data object
    - (int) the channel_id of the channel to verify
    - (int) the u_id of the user to verify
    - (int) the user status required (if the user is in the channel or not in the channel)
    """
    channel_obj = server_data.get_channel_by_id(channel_id)

    # If the user is needed in channel, throw error if not
    if status_required == const.USER_IN_CHANNEL:
        if not channel_obj.is_user_member(u_id):
            raise AccessError(description="User is not in channel")
    # If the usre is needed to be not in channel, throw error if is
    elif status_required == const.USER_NOT_IN_CHANNEL:
        if channel_obj.is_user_member(u_id):
            raise AccessError(description="User already in channel")
    else:
        raise InputError(description="ERROR: Unexpected Status_required value")
