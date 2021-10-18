#pylint: disable=C0301,R0915,W0105,R0914
#pylint: disable=R0801
'''
Test file for function channels_create
When testing this function, we assume that all other functions work as expected

Assumption:
- A channel could have duplicated name, but the id should be unique
'''
import urllib
import json
import pytest
import constants as const
from helper_functions_t import does_channel_exist_in_list, does_member_exist_in_list

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

'''
Pytest function to test invalid tokens being supplied into the function
- The channel should not be created, an AccessError should be thrown
'''
def test_invalid_tokens_public():
    """
    Pytest: testing channels_create with invalid token
    """

    # Testing creation of public channel
    # make up values for input
    token = "44444AFAFAFA"
    name = "testroom"
    is_public = True

    data = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    # this should throw HTTPError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(post_req)

def test_invalid_tokens_private():
    """
    Pytest: testing channels_create with invalid token
    """
    # Testing creation of private channel
    token = "1324440DDwWda"
    name = "testroom"
    is_public = False

    data = {
        "token": token,
        "name": name,
        "is_public": is_public,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    # this should throw HTTPError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(post_req)

"""
Using registered user initialized from auth_fixture to create a channel, but have invalid name inputs
"""
def test_invalid_name_input(auth_http_fixture):
    """
    Pytest: testing channels_create with invalid name
    """

    auth_fixture = auth_http_fixture

    #obtain the token first person in the initialization - richard
    token = auth_fixture[0]["token"]
    name = 'a' * 21

    data = {
        "token": token,
        "name": name,
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(post_req)

    data = {
        "token": token,
        "name": name,
        "is_public": False,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(post_req)

    #testing the same with another person
    token = auth_fixture[3]["token"]
    data = {
        "token": token,
        "name": name,
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(post_req)

    data = {
        "token": token,
        "name": name,
        "is_public": False,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(post_req)

"""
Using registered users to successfully create a channel, the channel should show up in the channels_list and channels_listall and operations regarding to the channel should succeed

The channel should be created with the correct information and can be found in the list
"""
def test_valid_channel_creation(auth_http_fixture):
    """
    Pytest: testing channels_create with valid channel creation
    """

    auth_fixture = auth_http_fixture
    # Split up the users
    user1 = auth_fixture[0]

    # register the first public channel for user1
    # Name: "COMP1000"
    # Channel ID: unknown, return from function
    channel_name = "COMP1000"

    data = {
        "token": user1["token"],
        "name": channel_name,
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)
    payload = json.load(response)

    channel_id = payload['channel_id']
    # check if the return contains the correct type
    assert isinstance(channel_id, int)

    # The channel is successfully created, it should show up in other functions
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)

    # The only channel that should returned is the channel that were created
    channel_list = payload["channels"]
    assert channel_list[0]["channel_id"] == channel_id
    assert channel_list[0]["name"] == "COMP1000"

    # Same thing should happen to channels_listall
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    payload = json.load(response)

    channel_list = payload["channels"]
    assert channel_list[0]["channel_id"] == channel_id
    assert channel_list[0]["name"] == "COMP1000"

    # register the second channel, first private channel for user1, it should not overwrite the previous channel
    # Name: "ENG1001"
    # Channel ID: unknown, return from function
    channel_name2 = "ENG1001"
    data = {
        "token": user1["token"],
        "name": channel_name2,
        "is_public": False,
    }
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)
    payload = json.load(response)

    channel_id2 = payload['channel_id']
    assert isinstance(channel_id2, int)

    # Now the user should have 2 channels in the list
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload = json.load(response)

    channel_list2 = payload["channels"]

    # The public channel should still exist
    assert does_channel_exist_in_list(channel_list2, channel_id, channel_name)
    assert does_channel_exist_in_list(channel_list2, channel_id2, channel_name2)

    # The channel ID and channel name should match
    assert not does_channel_exist_in_list(channel_list2, channel_id2, channel_name)
    assert not does_channel_exist_in_list(channel_list2, channel_id, channel_name2)

    # User1 should be the owner of the channel created
    token = user1["token"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)

    channel_owner_list = payload["owner_members"]
    channel_name3 = payload["name"]
    assert channel_name3 == channel_name

    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])

'''

if __name__ == "__main__":

    channel_list =[{ 
        "channel_id" : 0, "name": "COMP1001"
    }, { 
        "channel_id" : 1, "name": "ENG1001"
    }] 

    print (does_channel_exist_in_list(channel_list, 0, "COMP1001"))
    print (does_channel_exist_in_list(channel_list, 1, "COMP1001"))
    print (does_channel_exist_in_list(channel_list, 1, "ENG1001"))

    name = 'a' * 21
    print (name)

'''
