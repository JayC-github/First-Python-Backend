#pylint: disable=C0301, R0914, W0105
#pylint: disable=R0801
'''
Test file for function channels_list
When testing this function, we assume that all other functions work as expected
'''

import urllib
import json
import pytest
import constants as const
from helper_functions_t import does_channel_exist_in_list

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

"""
Invalid token test, should return AccessError
"""

def test_invalid_tokens():
    """
    Pytest: test channels_list with invalid tokens
    """

    # make up values for input
    token = "44444AFAFAFA"

    # this should throw AccessError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")

"""
Valid token tests with no channels, the users are pre-registered with fixture auth_fixture     
"""
def test_valid_token_no_channels(auth_http_fixture):
    """
    Pytest: test channels_list with invalid channels
    """

    auth_fixture = auth_http_fixture

    # Split up the users
    user1 = auth_fixture[0]
    user2 = auth_fixture[1]
    user3 = auth_fixture[2]
    user4 = auth_fixture[3]
    user5 = auth_fixture[4]

    # For each user, use channels_list function, no channels should return
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channel_list1 = payload["channels"]

    token = user2["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channel_list2 = payload["channels"]

    token = user3["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channel_list3 = payload["channels"]

    token = user4["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channel_list4 = payload["channels"]

    token = user5["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channel_list5 = payload["channels"]

    # The length of the returned list should be 0
    assert len(channel_list1) == 0
    assert len(channel_list2) == 0
    assert len(channel_list3) == 0
    assert len(channel_list4) == 0
    assert len(channel_list5) == 0

"""
Using valid token and created channels from the channels_fixture to test that channel_list should only list channels that the user is a part of, instead of all channels
"""

def test_valid_token_owned_channels(channels_http_fixture):
    """
    Pytest: test channels_list with owned channels
    """

    channels_fixture = channels_http_fixture

    #Split up the users:
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]

    #Extract the channel informations from the user
    channel_list1 = user1["channels"]
    channel_list2 = user2["channels"]


    # List channels for user 1
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channels_user1 = payload["channels"]

    # Check if it only contains the channels created by user1
    # user1 created two channels, COMP1531 and COMP2511, both public
    assert does_channel_exist_in_list(channels_user1, channel_list1[0]["channel_id"], channel_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user1, channel_list1[1]["channel_id"], channel_list1[1]["name"])

    # The channel name should match with the channel ID
    assert not does_channel_exist_in_list(channels_user1, channel_list1[0]["channel_id"], channel_list1[1]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list1[1]["channel_id"], channel_list1[0]["name"])

    # List channels for user 2
    token = user2["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)

    channels_user2 = payload["channels"]

    # Check if it only contains the channels created by user2
    # user2 created one channel, ENG1001 it is private but since user2 is authorized, they should still see it

    assert does_channel_exist_in_list(channels_user2, channel_list2[0]["channel_id"], channel_list2[0]["name"])

    # The channel name should match with the channel ID
    assert not does_channel_exist_in_list(channels_user2, channel_list2[0]["channel_id"], "something random")
    assert not does_channel_exist_in_list(channels_user2, 99983, channel_list2[0]["name"])

    # Can add more users here

def test_valid_token_not_owned_channels(channels_http_fixture):
    """
    Pytest: test channels_list with not owned channels
    """

    channels_fixture = channels_http_fixture

    #Split up the users:
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    #Extract the channel informations from the user
    channel_list2 = user2["channels"]
    channel_list3 = user3["channels"]
    channel_list4 = user4["channels"]
    channel_list5 = user5["channels"]

    # List channels for user 1
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channels_user1 = payload["channels"]

    # the channels from other users should not exist in this list
    # Because the user is not authorized
    assert not does_channel_exist_in_list(channels_user1, channel_list2[0]["channel_id"], channel_list2[0]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list3[0]["channel_id"], channel_list3[0]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list4[0]["channel_id"], channel_list4[0]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list5[0]["channel_id"], channel_list5[0]["name"])

"""
The channel list include the channels a user is member of 
"""
def test_valid_token_member_channel(channels_http_fixture):
    """
    Pytest: test channels_list with channels that user is a member of
    """

    channels_fixture = channels_http_fixture

    #Split up the users:
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]

    #Extract the channel informations from the user
    channel_list1 = user1["channels"]
    channel_list2 = user2["channels"]

    #Now invite user2 into user1's channel
    # List channels for user 1
    data = {
        "token": user1["token"],
        "channel_id": channel_list1[0]["channel_id"],
        "u_id": user2["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)

    #Now user 2 should contain 2 channels, one owned, one as member
    token = user2["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)
    channels_user2 = payload["channels"]

    assert does_channel_exist_in_list(channels_user2, channel_list1[0]["channel_id"], channel_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user2, channel_list2[0]["channel_id"], channel_list2[0]["name"])
