#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the channel_join function
'''
#pylint: disable=trailing-whitespace
#pylint: disable=line-too-long
#pylint: disable=unused-variable
#pylint: disable=too-many-locals

import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_channel_join(channels_http_fixture):
    ''' Tests channel join functionality '''
    channels_fixture = channels_http_fixture

    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[0]["channels"][1]["channel_id"]

    # Join channel with user
    data_join = json.dumps({
        "token": token,
        "channel_id": channel_id
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # Check channel_list for the user if they have successfully joined
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={token}")
    payload_list = json.load(response_list)

    channel_list_user = payload_list['channels']
    assert any(True for i in channel_list_user if i['channel_id'] == channel_id) 

def test_channel_join_invalid_channel_id(channels_http_fixture):
    '''
    Test case for invalid channel ID
    - channel does not exist
    '''
    channels_fixture = channels_http_fixture

    # set invalid channel_id
    token = channels_fixture[1]["token"]
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token}")
    all_channels = json.load(response_list)

    # as defined in data types where all variables with suffix _id will be an integer
    channel_ids = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_ids) + 1

    # try joining the invalid channel
    data_join = json.dumps({
        "token": token,
        "channel_id": invalid_channel_id
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req1)

def test_channel_join_double(channels_http_fixture):
    '''
    Test case for invalid channel ID
    - user is already part of the channel
    '''
    channels_fixture = channels_http_fixture

    # store channel id for a channel which the user is already a member of 
    token = channels_fixture[1]['token']
    dup_channel_id = channels_fixture[1]['channels'][0]['channel_id']

    # try joining a channel that has already been joined
    data_join = json.dumps({
        "token": token,
        "channel_id": dup_channel_id
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})  

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req)
 
def test_channel_join_private_non_admin(auth_http_fixture):
    '''
    Test case for private channel
    - user is not admin (default slack member)
    '''
    auth_fixture = auth_http_fixture

    token1 = auth_fixture[1]['token']  
    token2 = auth_fixture[2]['token']  

    # Create private channel with a user then see if another user (not admin) can join
    data_priv = json.dumps({
        "token": token1,
        "name": "A Private Channel",
        "is_public": False
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_priv, method='POST', headers={"Content-Type": "application/json"})
    response_priv = urllib.request.urlopen(req)
    priv_channel = json.load(response_priv)
    priv_channel_id = priv_channel['channel_id']

    # try joining the invalid channel
    data_join = json.dumps({
        "token": token2,
        "channel_id": priv_channel_id
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req1)

def test_channel_join_private_admin(auth_http_fixture):
    '''
    Test case for private channel
    - user is admin (slackrowner)
    '''
    auth_fixture = auth_http_fixture

    # store user data for slackrowner and normal user
    slackrtoken = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']  
    
    # Create private channel with a user1 then see if slackrowner can join
    data_priv = json.dumps({
        "token": token1,
        "name": "A Private Channel",
        "is_public": False
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_priv, method='POST', headers={"Content-Type": "application/json"})
    response_priv = urllib.request.urlopen(req)
    priv_channel = json.load(response_priv)
    priv_channel_id = priv_channel['channel_id']

    # try joining the channel with slackrowner
    data_join = json.dumps({
        "token": slackrtoken,
        "channel_id": priv_channel_id
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req1)

    # Check channel_list for the slackruser if they have successfully joined
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={slackrtoken}")
    payload_list = json.load(response_list)
    channel_list_slackrowner = payload_list['channels']

    # make sure channel exists in the list of slackrowners channels (if none can be found it means join did not work)
    assert any(True for i in channel_list_slackrowner if i['channel_id'] == priv_channel_id)

def test_channel_join_invalid_token(auth_http_fixture):
    '''
    Test case for invalid token
    '''
    auth_fixture = auth_http_fixture

    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']

    # set an invalid token 
    invalid_token = '12345'

    # Create channel with a user1
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    pub_channel_id = pub_channel['channel_id']

    # try joining the channel with an invalid token
    data_join = json.dumps({
        "token": invalid_token,
        "channel_id": pub_channel_id
    }).encode('utf-8')
    req1 = urllib.request.Request(f"{BASE_URL}/channel/join", data=data_join, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req1)
