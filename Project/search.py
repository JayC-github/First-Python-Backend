# pylint: disable=C0301, W0105
"""
################### search.py ####################
A file for the search function for the backend server

Will be using the following classes
server_data_class
channel_class
session_class
user_class
message_class
error

Contains functions:
search

"""

from error import AccessError
#from server_data_class import Server_data
#from channel_class import Channel
#from sessions_class import Sessions
#from channels import channels_create
#from message_class import Message

#from channels import channels_create
#from channel import channel_invite
#from tests.helper_functions_t import generate_messages

def search(server_data, token, query_str):
    """
    Search function:
    A function that search for the query string in all channels that the user has joined and return the message in time order

    input:
    - server_data (obj)
    - token (string)
    - query_str (string)

    Output:
    - {messages}

    """

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if not session_obj.is_token_active(token):
        raise AccessError(description="Invalid Token")

    # Get the user_id from the session
    u_id = session_obj.get_token_user(token)

    # Get all channels from the server_data
    channel_list = server_data.get_channel_list()
    # Obtain all channels that the user is in
    channels = []
    for channel in channel_list:
        if channel.is_user_member(u_id):
            channels.append(channel)

    # For each channel, do a search with query_str and get all message objects that matches
    message_obj_list = []
    for channel in channels:
        message_obj_list.extend(channel.message_search(query_str))

    # Sort the message objects
    message_obj_list.sort(key=lambda x: x.time_created, reverse=True)

    output = {
        "messages": []
    }
    # Output in the correct format
    for message_obj in message_obj_list:
        output["messages"].append(message_obj.pack_message_info(u_id))

    return output

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

    channel_obj = server_data.get_channel_by_id(channel_id2["channel_id"])

    message_list = generate_messages(60)
    for message in message_list:
        print (f"the message is: {message['message']}")
        channel_obj.add_message(message["message_id"], message["message"], u_id)

    # Testing begin
    result = search(server_data, token, "4")
    print (result)
'''