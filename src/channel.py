"""
################# s_channel_function.py ####################
A file for the channel related functions for the backend server

Using resources from:
server_data_class
channel_class
session_class
user_class
error

Contains functions:
channel_invite
channel_details
channel_messages
channel_join
channel_leave
channel_addowner
channel_removeowner
"""
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=W0212, W0105, W0612

import constants as const
from error import AccessError, InputError
from verification import verify_user_id, verify_n_get_valid_token, verify_channel_id, verify_user_channel_status, verify_user_channel_access
#from server_data_class import Server_data
#from channel_class import Channel
#from sessions_class import Sessions
#from channels import channels_create
#from tests.helper_functions_t import generate_messages

def channel_invite(server_data, token, channel_id, u_id):
    """
    channel_invite function
    a function that invites a user to join a channel, given that the user is valid and the token is valid
    
    input:
    - server_data (obj)
    - token (string)
    - channel_id (int)
    - u_id (int)
    
    output:
    - {}
    """
    
    # Verifying inputs
    verify_user_id(server_data, u_id)
    verify_channel_id(server_data, channel_id)
    u_id_from = verify_n_get_valid_token(server_data, token)
    verify_user_channel_access(server_data, channel_id, u_id, const.USER_NOT_IN_CHANNEL)

    # Get the target user object
    user_target = server_data.get_user_by_id(u_id)

    # Check if the user is already a part of the channel
    channel_obj = server_data.get_channel_by_id(channel_id)
    
        
    # Check if the user is in the channel
    verify_user_channel_status(server_data, channel_id, u_id_from, const.PERMISSION_LOCAL_MEMBER)

    # No more errors from now on, proceed to execute invitation
    user_info = user_target.get_user_member_info()
            
    # Check if the target user is owner of slackr
    if user_target.is_owner_of_slackr():
        # If user is owner of slackr, add owner and add member
        channel_obj.add_owner(user_info)
    else:
        # If user is regular member, add member
        channel_obj.add_member(user_info)
                
    return {}

            
def channel_details(server_data, token, channel_id):
    """
    channel_details function:
    A function that shows the details of a channel given a valid token, and that the user is authroized in the channel
    
    Input:
    - server_data (obj)
    - token (string)
    - channel_id (int)
    
    Output:
    - {name, owner_members, all_members}
    """
    
    # Check if the channel exists
    verify_channel_id(server_data, channel_id)

    # Verify token and get u_id
    u_id = verify_n_get_valid_token(server_data, token)

    # Verify if the user is a member of the channel
    verify_user_channel_status(server_data, channel_id, u_id, const.PERMISSION_LOCAL_MEMBER)

    # Update the channel's user list to ensure that it is up-to-date with the main user list
    update_channel_user_lists(server_data, channel_id)

    # Return the channel details
    channel_obj = server_data.get_channel_by_id(channel_id)
    rt_details = channel_obj.pack_channel_details()
    return rt_details


def channel_messages(server_data, token, channel_id, start):
    """
    channel_messages function
    a function that returns a list of messages from a channel, given the start point and a valid token
    
    Input:
    - server_data(obj)
    - token (string)
    - channel_id (int)
    - start (int)
    
    Output:
    - {messages, start, end}
    """
    
    # Check if the channel exists
    verify_channel_id(server_data, channel_id)
    
    # Check if the token is active
    u_id = verify_n_get_valid_token(server_data, token)

    channel_obj = server_data.get_channel_by_id(channel_id)
    if channel_obj.get_num_messages() == 0 and start == 0:
        return {
            "start": 0,
            "end": 0,
            "messages": [],
        }

    if start >= channel_obj.get_num_messages():
        raise InputError(description="Invalid start point")

    # Verify if the user is a member of the channel
    verify_user_channel_status(server_data, channel_id, u_id, const.PERMISSION_LOCAL_MEMBER)
        
    # All errors are detected, return the outcome as usual
    # Calculate the end point from the start
    end = start + 50
    if end > channel_obj.get_num_messages():
        end = -1
    
    # Get all message objects
    message_obj_list = channel_obj.get_message_range(start, end)
    
    rt_infos = {}
    rt_infos["start"] = start
    rt_infos["end"] = end
    rt_infos["messages"] = []
    
    for message_obj in message_obj_list:
        info = message_obj.pack_message_info(u_id)
        rt_infos["messages"].append(info)
        
    
    return rt_infos    
        
def channel_join(server_data, token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, adds them  to that channel 
    
    Input:
    - server_data(obj)
    - token (string)
    - channel_id (int)

    Output:
    - {}
    """

    # Check if the channel exists
    verify_channel_id(server_data, channel_id)
  
    # Verify if the token is active, and get u_id and channel_id from the active session
    u_id = verify_n_get_valid_token(server_data, token)
    # Verify if the user is not in channel
    verify_user_channel_access(server_data, channel_id, u_id, const.USER_NOT_IN_CHANNEL)

    channel_obj = server_data.get_channel_by_id(channel_id)
    # Check if user is already a member of the channel
    user_obj = server_data.get_user_by_id(u_id)
    user_info = user_obj.get_user_member_info()

    if user_obj.is_owner_of_slackr():
        # User is an owner of slack
        channel_obj._member_list.append(user_info) 
        channel_obj._owner_list.append(user_info) 
    else: 
        # User is not an owner of slack
        if channel_obj._is_public:
            # Public channel
            channel_obj._member_list.append(user_info)       
        else:
            # Private channel
            raise AccessError(description="User not authorised")


    return {}

def channel_leave(server_data, token, channel_id):
    """
    Given a channel_id, the user is removed as a member of this channel
    
    Input:
    - server_data(obj)
    - token (string)
    - channel_id (int)
    
    Output:
    - {}
    """

    # Check if the channel exists
    verify_channel_id(server_data, channel_id)

    # Verify token and get token if it is a valid session
    u_id = verify_n_get_valid_token(server_data, token)

    # Verify that the user is a member
    verify_user_channel_access(server_data, channel_id, u_id, const.USER_IN_CHANNEL)

    # Perform member removal
    channel_obj = server_data.get_channel_by_id(channel_id)
    channel_obj.remove_member(u_id) 
    return {}

def channel_addowner(server_data, token, channel_id, u_id):
    """
    Make user with user u_id an owner of this channel
    
    Input:
    - server_data(obj)
    - token (string)
    - channel_id (int)
    - u_id (int)
    
    Output:
    - {}
    """

    # Check if the channel exists
    verify_channel_id(server_data, channel_id)
   
    # Verify if token is active, and if so, get u_id from the active session
    u_id_owner = verify_n_get_valid_token(server_data, token)

    # Verify if the u_id_owner is a owner of the channel or owner of slacker
    verify_user_channel_status(server_data, channel_id, u_id_owner, const.PERMISSION_LOCAL_OWNER)
    
    channel_obj = server_data.get_channel_by_id(channel_id)        
    user_obj = server_data.get_user_by_id(u_id)
    # Is either slackr owner or channel owner
    # Now check if the user being added is already an owner
    if not channel_obj.is_user_owner(u_id): 
        assert channel_obj.add_owner(user_obj.get_user_member_info())
    else:
        raise InputError(description="User is already an owner")

    return {}

def channel_removeowner(server_data, token, channel_id, u_id):
    """
    Remove user with user u_id from an owner of this channel
    
    Input:
    - server_data(obj)
    - token (string)
    - channel_id (int)
    - u_id (int)
    
    Output:
    - {}
    """

    # Check if the channel exists
    verify_channel_id(server_data, channel_id)
        
    channel_obj = server_data.get_channel_by_id(channel_id)
        
    # Verify the token and get u_id from the active token
    u_id_owner = verify_n_get_valid_token(server_data, token)
    user_obj_owner = server_data.get_user_by_id(u_id_owner)

    # Verify if the u_id_owner is a owner of the channel or owner of slacker
    verify_user_channel_status(server_data, channel_id, u_id_owner, const.PERMISSION_LOCAL_OWNER)
            
    if channel_obj.is_user_owner(u_id):
        channel_obj.remove_owner(u_id) 
    else:
        # user is not an owner of the channel
        raise InputError(description="User is not an owner of the channel")

    return {}

def update_channel_user_lists(server_data, channel_id):
    """
    A function to update the channel of their user informations

    Input:
    - (int) channel_id to update

    Output:
    {}
    """
    channel_obj = server_data.get_channel_by_id(channel_id)

    #Update the members' data
    for user in channel_obj._member_list:
        #Get the latest user data for the current user
        latest_user_data = server_data.get_user_by_id(user["u_id"])

        #Update the data that is stored in the member list
        user["name_first"] = latest_user_data.name_first
        user["name_last"] = latest_user_data.name_last
        user["profile_img_url"] = latest_user_data.profile_img_url

    #Update the owners' data
    for user in channel_obj._owner_list:
        #Get the latest user data for the current user
        latest_user_data = server_data.get_user_by_id(user["u_id"])

        #Update the data that is stored in the owner list
        user["name_first"] = latest_user_data.name_first
        user["name_last"] = latest_user_data.name_last
        user["profile_img_url"] = latest_user_data.profile_img_url

    return {}

'''
if __name__ == "__main__":

    # Add two users
    server_data = Server_data()
    u_id = server_data.new_user("richard@gmail.com", "12345", "Richard", "Park", "richardpark", 1)
    token = "ABCDE"

    sessions = server_data.get_sessions_list()
    sessions.create_active_session(u_id, token)

    u_id2 = server_data.new_user("steven@gmail.com", "12345", "Steven", "Yang", "stevenyang", 2)
    token2 = "CDEFG"
    sessions.create_active_session(u_id2, token2)

    channel_id1 = channels_create(server_data, token, "TEST1", True)

    details = channel_details(server_data, token, channel_id1["channel_id"])
    #print (details)

    channel_invite(server_data, token, channel_id1["channel_id"], u_id2)
    details = channel_details(server_data, token, channel_id1["channel_id"])

    channel_obj = server_data.get_channel_by_id(channel_id1["channel_id"])

    message_list = generate_messages(60)
    for message in message_list:
        channel_obj.add_message(message["message_id"], message["message"], u_id)

    messages = channel_messages(server_data, token, channel_id1["channel_id"], 10)
    #print (details)

    print (messages)
'''
    
