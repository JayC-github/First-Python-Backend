#pylint: disable=C0301,R0914,W0105,R0915
#pylint: disable=R0801
'''
Test file for function channels_listall
When testing this function, we assume that all other functions work as expected

Assumptions:
channels_listall will show all channels, including the private channels
'''

import urllib
import json
import pytest
import constants as const
from helper_functions_t import does_channel_exist_in_list

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

# Testing invalid token with pre-filled fixture with 5 registered users, should still return AccessError
def test_http_invalid_token_with_users():
    """
    Pytest: testing with invalid token
    """

    token = "AMADEUPTOKEN2"

    # this should throw AccessError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")

def test_token_with_no_channels(auth_http_fixture):
    """
    Pytest: testing with no channels
    """

    # Import the token infos
    user1 = auth_http_fixture[0]
    user2 = auth_http_fixture[1]
    user3 = auth_http_fixture[2]
    user4 = auth_http_fixture[3]
    user5 = auth_http_fixture[4]

    # User 1 Listall
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user1 = payload["channels"]

    # User 2 Listall
    token = user2["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user2 = payload["channels"]

    # User 3 Listall
    token = user3["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)
    channels_user3 = payload["channels"]

    # User 4 Listall
    token = user4["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user4 = payload["channels"]

    # User 5 Listall
    token = user5["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user5 = payload["channels"]

    # All of them should be empty
    assert len(channels_user1) == 0
    assert len(channels_user2) == 0
    assert len(channels_user3) == 0
    assert len(channels_user4) == 0
    assert len(channels_user5) == 0

"""
Because the function shows all channels, it should show every channel that has been created
"""
def test_token_with_channels(channels_http_fixture):
    """
    Pytest: testing with channels
    """

    # Import the user info
    user1 = channels_http_fixture[0]
    user2 = channels_http_fixture[1]
    user3 = channels_http_fixture[2]
    user4 = channels_http_fixture[3]
    user5 = channels_http_fixture[4]

    # Extract the channel info from users
    channels_list1 = user1["channels"]
    channels_list2 = user2["channels"]
    channels_list3 = user3["channels"]
    channels_list4 = user4["channels"]
    channels_list5 = user5["channels"]

    # Each of the listall should contain the same thing
    # user1
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user = payload["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    # user2
    token = user2["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user = payload["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    # user3
    token = user3["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user = payload["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    #user4
    token = user4["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user = payload["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    #user5
    token = user4["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user = payload["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

"""
Testing channels_listall should return the same after changes in membership/ownership 
"""
def test_token_with_channels_n_changes(channels_http_fixture):
    """
    Pytest: testing with channels and changes
    """

    # Import the user info
    user1 = channels_http_fixture[0]
    user2 = channels_http_fixture[1]
    user3 = channels_http_fixture[2]
    user4 = channels_http_fixture[3]
    user5 = channels_http_fixture[4]

    # Extract the channel info from users
    channels_list1 = user1["channels"]
    channels_list2 = user2["channels"]
    channels_list3 = user3["channels"]
    channels_list4 = user4["channels"]
    channels_list5 = user5["channels"]

    # Making several changes to membership and ownership
    # Add user5 to COMP1531
    # Remove user1 from COMP1531
    # add user2 to COMP3221
    # remove user4 to COMP3221

    data = {
        "token": user1["token"],
        "channel_id": channels_list1[0]["channel_id"],
        "u_id": user5["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channel/addowner", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)

    data = {
        "token": user4["token"],
        "channel_id": channels_list4[0]["channel_id"],
        "u_id": user2["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channel/addowner", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)

    data = {
        "token": user1["token"],
        "channel_id": channels_list1[0]["channel_id"],
        "u_id": user1["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)

    data = {
        "token": user4["token"],
        "channel_id": channels_list4[0]["channel_id"],
        "u_id": user4["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)


    #The list of channels should remain the same
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channels_user = payload["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])
