# pylint: disable=C0301, W0105
"""
############### standup.py ##################
a file that implements the standup features for the backend server

"""

#from server_data_class import Server_data
#from channel_class import Channel
#from user_class import User
from error import AccessError, InputError

#from channels import channels_create
#from channel import channel_invite
#from time_stamp import get_timestamp_now

def standup_start(server_data, token, channel_id, length):
    """
    standup_start
    A function that starts a standup in a channel

    Input:
    - (str) token
    - (int) channel_id
    - (int) length of the standup
    Output:
    - {time_finish}
    """

    # Check if the channel exists
    if not server_data.does_channel_exist(channel_id):
        raise InputError(description="Invalid channel")

    channel_obj = server_data.get_channel_by_id(channel_id)

    if channel_obj.is_standup_active:
        raise InputError(description="Active standup is currently running")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if not session_obj.is_token_active(token):
        raise AccessError(description="Invalid Token")

    # Get user_id on token
    u_id = session_obj.get_token_user(token)

    time_finish = channel_obj.activate_standup(length, u_id)

    rt_dic = {
        "time_finish": time_finish,
    }
    return rt_dic

def standup_send(server_data, token, channel_id, message):
    """
    standup_send
    A function that sends message into an active standup

    Input:
    - (str) token
    - (int) channel_id
    - (str) message to send
    Output:
    - {}
    """
    # Check if the channel exists
    if not server_data.does_channel_exist(channel_id):
        raise InputError(description="Invalid channel")

    channel_obj = server_data.get_channel_by_id(channel_id)

    if not channel_obj.is_standup_active:
        raise InputError(description="No standup is currently running")

    if len(message) > 1000:
        raise InputError(description="Message too long")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()
    # Check if the token is active
    if not session_obj.is_token_active(token):
        raise AccessError(description="Invalid Token")

    # Get user_id on token
    u_id = session_obj.get_token_user(token)

    if not channel_obj.is_user_member(u_id):
        raise AccessError(description="No permission to channel")

    user_obj = server_data.get_user_by_id(u_id)

    # All error's cleared
    channel_obj.add_standup_record(user_obj.handle, message)
    return {}

def standup_active(server_data, token, channel_id):
    """
    standup_active
    A function that checks if a standup is currently active in channel

    Input:
    - (str) token
    - (int) channel_id
    Output:
    - {is_active, time_finish}
    """
    # Check if the channel exists
    if not server_data.does_channel_exist(channel_id):
        raise InputError(description="Invalid channel")

    channel_obj = server_data.get_channel_by_id(channel_id)

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()
    # Check if the token is active
    if not session_obj.is_token_active(token):
        raise AccessError(description="Invalid Token")

    return_info = {
        "is_active": channel_obj.is_standup_active,
        "time_finish": channel_obj.time_finish,
    }

    return return_info

# Assumption: if a user exits the channel before standup finishes, the standup will be posted by such user as normal
def end_standup(server_data, channel_id):
    """
    end_standup
    A function that process the standup after it is over
    """
    # Obtain a message_id
    message_id = server_data.generate_message_id()

    channel_obj = server_data.get_channel_by_id(channel_id)
    channel_obj.end_standup(message_id)

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
    channel_id2 = channels_create(server_data, token, "TEST2", True)

    channel_invite(server_data, token, channel_id1["channel_id"], u_id2)
    dt = get_timestamp_now()

    standup_start(server_data, token, channel_id1["channel_id"], 20)

    print (standup_active(server_data, token, channel_id1["channel_id"]))
    print (standup_active(server_data, token, channel_id2["channel_id"]))

    standup_send(server_data, token, channel_id1["channel_id"], "testing first message")
    standup_send(server_data, token2, channel_id1["channel_id"], "testing second message")

    end_standup(server_data, channel_id1["channel_id"])
    msg = server_data.find_message_by_message_id(0)
    print(msg.message)
'''
