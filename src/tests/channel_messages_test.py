#pylint: disable=C0301, W0105, R0913, R0914
#pylint: disable=R0801
'''
Test file for channel_messages
When testing this function, we assume that all other functions work as expected

Assumptions:
- if a channel is empty, a call with start index 0 will return an empty message list.
'''

import pytest
from error import InputError, AccessError
from channel import channel_messages
from message import message_send
from helper_functions_t import generate_messages

'''
Helper function to check all messages
Need testing with real data

The function takes in a token, a u_id, a channel dictionary, a start point and a number of messages to generate num of messages to feed into the channel
Then it compare the specific block from start_point
'''

def check_and_compare_messages(server_data, token, u_id, channel, start_point, num_messages):
    """
    Function to generate message and check if the messages function behaves correctly
    """

    # We have a start point, create a theoretical end point
    end_index = start_point + 49
    total_msg_at_end_index = end_index + 1

    # Generate messages
    msg_info_list = generate_messages(num_messages)

    # Fill the channel with messages
    for message_info in msg_info_list:
        rt_info = message_send(server_data, token, channel["channel_id"], message_info["message"])
        message_info["message_id"] = rt_info["message_id"]

    # Collect messages
    rt_info = channel_messages(server_data, token, channel["channel_id"], start_point)
    end = rt_info["end"]
    record_list = rt_info["messages"]

    # Check if start and end is correct
    #assert start == start_point

    # If the the start point is within 50 messages of the end, return -1, if not, return start_point + 50
    if total_msg_at_end_index >= num_messages:
        assert end == -1
    else:
        # We put 50 here because it is 1 after the last of the batch, 49+1
        assert end == start_point + 50

    # Flip the list generation to put the most recent to the first in list
    msg_info_check_list = msg_info_list[::-1]
    assert len(msg_info_check_list) == num_messages

    # Check the length of the return list
    if total_msg_at_end_index >= num_messages:
        assert len(record_list) == num_messages - start_point
    else:
        assert len(record_list) == 50

    # Check if each message is at the correct position
    count = 0
    pos = start_point
    while count < len(record_list):

        # Load message to compare
        record = record_list[count]
        message_info = msg_info_check_list[pos]

        # Check if u_id matches
        assert record["u_id"] == u_id

        # Check if message id and message matches
        assert record["message_id"] == message_info["message_id"]
        assert record["message"] == message_info["message"]

        count += 1
        pos += 1

def test_channel_messages_invalid_token(channels_fixture):
    """
    pytest: testing channel_messages with invalid token
    """

    (server_data, channels_fixture) = channels_fixture

    channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    token = "AMADEUPTOKEN"
    start = 0

    # this should throw AccessError as the token is invalid
    with pytest.raises(AccessError):
        channel_messages(server_data, token, channel_id, start)

'''
Assumption:
We assume that if a channel is empty, by calling 0 as index will not incur an error, instead return an empty messages
'''
def test_channel_messages_invalid_channel(channels_fixture):
    """
    pytest: testing channel_messages with invalid channel
    """

    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[0]["token"]
    channel_id = 518951
    start = 0

    # this should throw AccessError as the token is invalid
    with pytest.raises(InputError):
        channel_messages(server_data, token, channel_id, start)

# Since the channels are empty, there is no start
def test_channel_messages_invalid_start_point(channels_fixture):
    """
    pytest: testing channel_messages with invalid start point
    """

    (server_data, channels_fixture) = channels_fixture

    token = channels_fixture[0]["token"]
    channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    start = 5

    # this should throw AccessError as the token is invalid
    with pytest.raises(InputError):
        channel_messages(server_data, token, channel_id, start)

def test_channel_messages_no_permission(channels_fixture):
    """
    pytest: testing channel_messages with no permission
    """

    (server_data, channels_fixture) = channels_fixture

    # Select user and channel
    token = channels_fixture[3]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[2]["channels"][0]

    with pytest.raises(AccessError):
        check_and_compare_messages(server_data, token, u_id, channel, 0, 30)

# Test for less than 50 messages
# The function should return start with 0, end with -1 and 50 messages total
def test_channel_messages_0_to_30_messages(channels_fixture):
    """
    pytest: testing channel_messages with 0-30 messages
    """

    (server_data, channels_fixture) = channels_fixture
    # Select user and channel
    token = channels_fixture[0]["token"]
    u_id = channels_fixture[0]["u_id"]
    channel = channels_fixture[0]["channels"][0]

    check_and_compare_messages(server_data, token, u_id, channel, 0, 30)

def test_channel_messages_index_5_29(channels_fixture):
    """
    pytest: testing channel_messages with 5-29 messages
    """

    (server_data, channels_fixture) = channels_fixture

    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(server_data, token, u_id, channel, 5, 30)

def test_channel_messages_index_0_49_w_51_messages(channels_fixture):
    """
    pytest: testing channel_messages with 0-49 messages
    """

    (server_data, channels_fixture) = channels_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(server_data, token, u_id, channel, 0, 51)

def test_channel_messages_index_0_49_w_200_messages(channels_fixture):
    """
    pytest: testing channel_messages with 0-49 messages
    """

    (server_data, channels_fixture) = channels_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(server_data, token, u_id, channel, 0, 200)

def test_channel_messages_index_100_149_w_200_messages(channels_fixture):
    """
    pytest: testing channel_messages with 100-149 messages
    """

    (server_data, channels_fixture) = channels_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(server_data, token, u_id, channel, 100, 200)

def test_channel_messages_index_160_199_w_200_messages(channels_fixture):
    """
    pytest: testing channel_messages with 160-199 messages
    """

    (server_data, channels_fixture) = channels_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(server_data, token, u_id, channel, 160, 200)
