#pylint: disable=C0301, R0914, W0105
#pylint: disable=R0801
'''
Test file for channel_messages
When testing this function, we assume that all other functions work as expected

Assumptions:
- if a channel is empty, a call with start index 0 will return an empty message list.
'''
import urllib
import json
import pytest
import constants as const

#from channel import channel_invite, channel_details, channel_messages
#from message import message_send
from helper_functions_t import generate_messages

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

'''
Helper function to check all messages
Need testing with real data

The function takes in a token, a u_id, a channel dictionary, a start point and a number of messages to generate num of messages to feed into the channel
Then it compare the specific block from start_point
'''

def check_and_compare_messages(token, u_id, channel, start_point, num_messages):
    """
    a function to check and compare message with given infos
    """

    # We have a start point, create a theoretical end point
    end_index = start_point + 49
    total_msg_at_end_index = end_index + 1

    # Generate messages
    msg_info_list = generate_messages(num_messages)

    # Fill the channel with messages
    for message_info in msg_info_list:

        data = {
            "token": token,
            "channel_id": channel["channel_id"],
            "message": message_info["message"],
        }
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
        response = urllib.request.urlopen(req)
        payload = json.load(response)

        message_info["message_id"] = payload["message_id"]

    # Collect messages
    channel_id = channel["channel_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start={start_point}")
    payload = json.load(response)

    end = payload["end"]
    record_list = payload["messages"]

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

def test_channel_messages_invalid_token(channels_http_fixture):
    """
    pytest: test channel_messages with invalid token
    """

    channels_fixture = channels_http_fixture

    channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    token = "AMADEUPTOKEN"
    start = 0

    # this should throw AccessError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start={start}")

"""
Assumption:
We assume that if a channel is empty, by calling 0 as index will not incur an error, instead return an empty messages
"""
def test_channel_messages_invalid_channel(channels_http_fixture):
    """
    pytest: test channel_messages with invalid channel
    """

    channels_fixture = channels_http_fixture
    token = channels_fixture[0]["token"]
    channel_id = 518951
    start = 0
    # this should throw AccessError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start={start}")

# Since the channels are empty, there is no start
def test_channel_messages_invalid_start_point(channels_http_fixture):
    """
    pytest: test channel_messages with invalid start point
    """

    channels_fixture = channels_http_fixture

    token = channels_fixture[0]["token"]
    channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    start = 200

    data = {
        "token": token,
        "channel_id": channel_id,
        "start": start,
    }
    json_data = json.dumps(data).encode('utf-8')
    urllib.request.Request(f"{BASE_URL}/channel/messages", method="GET", data=json_data, headers={"Content-Type": "application/json"})


    # this should throw AccessError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channel/messages?token={token}&channel_id={channel_id}&start={start}")

def test_channel_messages_no_permission(channels_http_fixture):
    """
    pytest: test channel_messages with no permission
    """

    channels_fixture = channels_http_fixture

    # Select user and channel
    token = channels_fixture[3]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[2]["channels"][0]

    with pytest.raises(urllib.error.HTTPError):
        check_and_compare_messages(token, u_id, channel, 0, 30)

# Test for less than 50 messages
# The function should return start with 0, end with -1 and 50 messages total
def test_channel_messages_0_to_30_messages(channels_http_fixture):
    """
    pytest: test channel_messages with 0 - 30 index
    """

    channels_fixture = channels_http_fixture
    # Select user and channel
    token = channels_fixture[0]["token"]
    u_id = channels_fixture[0]["u_id"]
    channel = channels_fixture[0]["channels"][0]

    check_and_compare_messages(token, u_id, channel, 0, 30)

def test_channel_messages_index_5_29(channels_http_fixture):
    """
    pytest: test channel_messages with 5-29 index
    """

    channels_fixture = channels_http_fixture

    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(token, u_id, channel, 5, 30)

def test_channel_messages_index_0_49_w_51_messages(channels_http_fixture):
    """
    pytest: test channel_messages with 0-49 index with 51 messages
    """

    channels_fixture = channels_http_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(token, u_id, channel, 0, 51)

def test_channel_messages_index_0_49_w_200_messages(channels_http_fixture):
    """
    pytest: test channel_messages with 0-49 index with 200 messages
    """

    channels_fixture = channels_http_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(token, u_id, channel, 0, 200)

def test_channel_messages_index_100_149_w_200_messages(channels_http_fixture):
    """
    pytest: test channel_messages with 100-149 index with 200 messages
    """

    channels_fixture = channels_http_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(token, u_id, channel, 100, 200)

def test_channel_messages_index_160_199_w_200_messages(channels_http_fixture):
    """
    pytest: test channel_messages with 160-199 index with 200 messages
    """

    channels_fixture = channels_http_fixture
    # Select user and channel
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[1]["u_id"]
    channel = channels_fixture[1]["channels"][0]

    check_and_compare_messages(token, u_id, channel, 160, 200)
