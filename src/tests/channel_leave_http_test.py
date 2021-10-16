#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the channel_leave function
'''
#pylint: disable=trailing-whitespace
#pylint: disable=line-too-long
#pylint: disable=too-many-locals
#pylint: disable=unused-variable
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_channel_leave(channels_http_fixture):
    '''
    Test case for a simple channel leave
    - user should not be in the list for that channel after they leave
    '''
    channels_fixture = channels_http_fixture
 
    # get user and channel details
    token = channels_fixture[1]['token']
    channel_id = channels_fixture[1]['channels'][0]['channel_id']

    # leave channel with user
    data_leave = json.dumps({
        "token": token,
        "channel_id": channel_id
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data_leave, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # now check whether in the list of channels for that user the removed channel exists
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload_list = json.load(response_list)
    list_channels = payload_list['channels']

    assert not any(True for x in list_channels if x['channel_id'] == channel_id)

def test_channel_leave_invalid_channel_id(channels_http_fixture):
    '''
    Test case for invalid channel ID
    - channel does not exist
    '''
    channels_fixture = channels_http_fixture

    # set invalid channel_id by checking channel lists
    token = channels_fixture[1]["token"]
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    all_channels = json.load(response_list)
    # as defined in data types where all variables with suffix _id will be an integer
    channel_ids = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_ids) + 1

    # leave channel with user
    data_leave = json.dumps({
        "token": token,
        "channel_id": invalid_channel_id
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data_leave, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req1)

def test_channel_leave_not_member(channels_http_fixture):
    '''
    Test case for when user is not part of channel
    '''
    channels_fixture = channels_http_fixture

    # store channel id for a channel which the user is not a member of 
    token1 = channels_fixture[1]['token']
    token2 = channels_fixture[2]['token']

    # create 2 channels and try leaving for a user that is not a member

    # create public channel with a user
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    pub_channel_id = pub_channel['channel_id']

    # create private channel with a user
    data_priv = json.dumps({
        "token": token1,
        "name": "A Private Channel",
        "is_public": False
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_priv, method='POST', headers={"Content-Type": "application/json"})
    response_priv = urllib.request.urlopen(req1)
    priv_channel = json.load(response_priv)
    priv_channel_id = priv_channel['channel_id']

    # leave public channel with user
    data_leave1 = json.dumps({
        "token": token2,
        "channel_id": pub_channel_id
    }).encode('utf-8')
    req_leave1 = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data_leave1, method='POST', headers={"Content-Type": "application/json"})

    # leave private channel with user
    data_leave2 = json.dumps({
        "token": token2,
        "channel_id": priv_channel_id
    }).encode('utf-8')
    req_leave2 = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data_leave2, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_leave1)

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_leave2)

def test_channel_leave_invalid_token(auth_http_fixture):
    '''
    Test case for invalid token
    '''
    auth_fixture = auth_http_fixture

    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']

    # set an invalid token 
    invalid_token = '12345'

    # Create a channel with a user1
    data_create = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_create, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    pub_channel_id = pub_channel['channel_id']

    # User 2 joins the channel
    data_join = json.dumps({
        "token": token2,
        "channel_id": pub_channel_id
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req1)

    # user2 tries to leave with invalid token
    data_leave = json.dumps({
        "token": invalid_token,
        "channel_id": pub_channel_id
    }).encode('utf-8')
    req_leave = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data_leave, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_leave)
