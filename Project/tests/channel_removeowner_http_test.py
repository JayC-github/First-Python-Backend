#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the channel_removeowner function
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

def test_channel_removeowner(auth_http_fixture):
    '''
    Test case for a simple channel removeowner
    - owner removing another owner in the same channel
    '''
    auth_fixture = auth_http_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channels with user1 then add user2 as owner
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

    # user1 adds user2 to public channel as an owner
    data_addownerpub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_addownerpub = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addownerpub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addownerpub)

    # user1 adds user2 to private channel as an owner
    data_addownerpriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_addownerpriv = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addownerpriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addownerpriv)

    # user1 removes user2 from owner permissions in public channel
    data_rmvownerpub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_rmvownerpub = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvownerpub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_rmvownerpub)

    # user1 removes user2 from owner permissions in public channel
    data_rmvownerpriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_rmvownerpriv = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvownerpriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_rmvownerpriv)

    # check channel details to make sure user 2 is a non owner member
    # channel1 details for user2
    response_channel_det1 = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token2}&channel_id={pub_channel_id}")
    payload1 = json.load(response_channel_det1)
    channel_det1 = payload1['owner_members']

    # channel2 details for user2
    response_channel_det2 = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token2}&channel_id={priv_channel_id}")
    payload2 = json.load(response_channel_det2)
    channel_det2 = payload2['owner_members']    

    # owner member list should not have any ids equal to the id of user2 
    assert not any(True for i in channel_det1 if i['u_id'] == uid2)
    assert not any(True for i in channel_det2 if i['u_id'] == uid2)

def test_channel_removeowner_invalid_channel_id(channels_http_fixture):
    '''
    Test case for invalid channel ID 
    '''
    channels_fixture = channels_http_fixture

    # get user details
    token_owner1 = channels_fixture[1]["token"]
    uid_owner2 = channels_fixture[2]["u_id"]

    # create channels with user1 then add user2 as owner
    # user1 creates a channel
    data_pub = json.dumps({
        "token": token_owner1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']
        
    #user1 adds user2 as an owner
    data_addowner = json.dumps({
        "token": token_owner1,
        "channel_id": channel_id,
        "u_id": uid_owner2
    }).encode('utf-8')
    req_addowner = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addowner)

    # get list of all channels
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token_owner1}")
    all_channels = json.load(response_list)

    # as defined in data types where all variables with suffix _id will be an integer
    channel_id_list = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_id_list) + 1

    # check if removeowner works with a valid user but invalid channel id
    data_rmvowner = json.dumps({
        "token": token_owner1,
        "channel_id": invalid_channel_id,
        "u_id": uid_owner2
    }).encode('utf-8')
    req_rmvowner = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvowner, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmvowner)

def test_channel_removeowner_not_owner(auth_http_fixture):
    '''
    Test case for removing user when user is not an owner of the channel
    '''
    auth_fixture = auth_http_fixture

    # user1 and create a channel (user1 will be owner of channel)
    token1 = auth_fixture[1]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channel with 1 user (user 1 is owner)
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']

    # user1 invites user2 as member
    data_invite = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_invite = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invite, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invite)

    # user1 removes user2 as owner (InputError should pop up)
    data_rmvowner = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_rmvowner = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvowner, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmvowner)

def test_channel_removeowner_user_not_channel_owner(auth_http_fixture):
    '''
    Test case when authorised user is not an owner of the channel and is not an owner of the slackr
    '''
    auth_fixture = auth_http_fixture

    # get user data
    token1 = auth_fixture[1]['token']
    token3 = auth_fixture[3]['token']
    uid2 = auth_fixture[2]['u_id']
    uid3 = auth_fixture[3]['u_id']

    # create channels with 1 user (user 1 is owner)
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

    # user2 joins as owner
    # user1 adds user2 as owner to public channel
    data_addowner1 = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_addowner1 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner1, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addowner1)

    # user1 adds user2 as owner to private channel
    data_addowner2 = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_addowner2 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner2, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addowner2)

    # user1 invites user3 to channels
    # user1 invites user3 to public channel
    data_invite1 = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": uid3
    }).encode('utf-8')
    req_invite1 = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invite1, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invite1)

    # user1 invites user3 to private channel
    data_invite2 = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": uid3
    }).encode('utf-8')
    req_invite2 = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invite2, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invite2)

    # user3 tries to remove user2 from ownership
    data_rmvowner1 = json.dumps({
        "token": token3,
        "channel_id": pub_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_rmvowner1 = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvowner1, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmvowner1)

    data_rmvowner2 = json.dumps({
        "token": token3,
        "channel_id": priv_channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_rmvowner2 = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvowner2, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmvowner2)

def test_channel_removeowner_invalid_token(auth_http_fixture):
    '''
    Test case for invalid token
    '''
    auth_fixture = auth_http_fixture
    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']
    uid2 = auth_fixture[2]['u_id']
    
    # set an invalid token 
    invalid_token = '12345'

    # user1 creates channels
    data_create = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_create, method='POST', headers={"Content-Type": "application/json"})
    response_channel = urllib.request.urlopen(req)
    channel = json.load(response_channel)
    channel_id = channel['channel_id']

    # user1 adds user2 as an owner
    data_addowner = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_addowner = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addowner)

    # user1 trys to remove user2 as owner with invalid token
    data_rmvowner = json.dumps({
        "token": invalid_token,
        "channel_id": channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_rmvowner = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data_rmvowner, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmvowner)
