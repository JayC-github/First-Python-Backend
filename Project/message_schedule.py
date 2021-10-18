# pylint: disable=C0301
"""
################## Message_schedule.py #######################
A file for the implementation of message scheduling
"""

from error import AccessError, InputError
from time_stamp import get_timestamp_now

# Process message info for message_sendlater - Special function
def process_message_infos(server_data, token, channel_id, message, time_sent):
    """
    process_message_infos
    a function that proccess a send later request, produces the necessary information to push into the waiting queue

    Input:
    - (str) token
    - (int) channel_id
    - (str) message
    - (int) time_send

    Output:
    - (dic) {message_id, channel_id, message, u_id, time_sent}
    """
    # Check if the channel exists
    if not server_data.does_channel_exist(channel_id):
        raise InputError(description="Invalid channel")

    if len(message) > 1000:
        raise InputError(description="Message too long")

    if time_sent < get_timestamp_now():
        raise InputError(description="Time is in the past")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if not session_obj.is_token_active(token):
        raise AccessError(description="Invalid Token")

    # Get u_id from the active session
    u_id = session_obj.get_token_user(token)
    channel_obj = server_data.get_channel_by_id(channel_id)

    if not channel_obj.is_user_member(u_id):
        raise AccessError

    # All checks complete, now compose data
    # Allocate a message_id to the scheduled message
    message_id = server_data.generate_message_id()

    # Compose them into a dic
    message_info = {
        "message_id": message_id,
        "channel_id": channel_id,
        "message": message,
        "u_id": u_id,
        "time_sent": time_sent,
    }

    return message_info

def send_delayed_message(server_data, message_infos):
    """
    send_delayed_message
    a function that sends out a delayed mesasge after it reaches the scheduled time

    Input:
    - (dics) {message_id, channel_id, message, u_id, time_sent}
    Output:
    - None
    """

    channel_id = message_infos["channel_id"]
    message_id = message_infos["message_id"]
    message = message_infos["message"]
    u_id = message_infos["u_id"]

    channel_obj = server_data.get_channel_by_id(channel_id)
    channel_obj.add_message(message_id, message, u_id)
