#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the channel_addowner function
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
#pylint: disable=too-many-locals
#pylint: disable=too-many-statements
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_channel_addowner(auth_http_fixture):
    '''
    Test case for a simple channel addowner
    - owner adding non member or member of channel as owner
    '''
    auth_fixture = auth_http_fixture

    # get user list
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    token3 = auth_fixture[3]['token']
    u_id2 = auth_fixture[2]['u_id']
    u_id3 = auth_fixture[3]['u_id']

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

    # add user2 as member
    data_invitepub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_invitepub = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invitepub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invitepub)

    data_invitepriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_invitepriv = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invitepriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invitepriv)

    # add user2 as owner (channel member -> channel owner)
    data_addownerpub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_addownerpub = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addownerpub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addownerpub)

    data_addownerpriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_addownerpriv = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addownerpriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addownerpriv)

    # add user3 as owner (channel non-member -> channel owner)
    data_nonmempub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id3
    }).encode('utf-8')
    req_nonmempub = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_nonmempub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_nonmempub)

    data_nonmenpriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id3
    }).encode('utf-8')
    req_nonmenpriv = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_nonmenpriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_nonmenpriv)

    # get details of channels
    # channel1 details for user2
    response_channel_det1 = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token2}&channel_id={pub_channel_id}")
    payload1 = json.load(response_channel_det1)
    channel_det1 = payload1['owner_members']

    # channel2 details for user2
    response_channel_det2 = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token2}&channel_id={priv_channel_id}")
    payload2 = json.load(response_channel_det2)
    channel_det2 = payload2['owner_members']

    # channel1 details for user3
    response_channel_det3 = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token3}&channel_id={pub_channel_id}")
    payload3 = json.load(response_channel_det3)
    channel_det3 = payload3['owner_members']

    # channel2 details for user3
    response_channel_det4 = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token3}&channel_id={priv_channel_id}")
    payload4 = json.load(response_channel_det4)
    channel_det4 = payload4['owner_members']

    # check that user2 and user3 are both owners for each channel
    assert any(True for i in channel_det1 if i['u_id'] == u_id2)
    assert any(True for i in channel_det2 if i['u_id'] == u_id2)
    assert any(True for i in channel_det3 if i['u_id'] == u_id3)
    assert any(True for i in channel_det4 if i['u_id'] == u_id3)

def test_channel_addowner_invalid_channel_id(channels_http_fixture):
    '''
    Test case for invalid channel ID 
    - channel id does not exist
    '''
    channels_fixture = channels_http_fixture

    # get user details
    token_owner = channels_fixture[1]["token"]
    u_id_non_owner = channels_fixture[2]["u_id"]
    response_list = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={token_owner}")
    all_channels = json.load(response_list)

    # as defined in data types where all variables with suffix _id will be an integer
    channel_ids = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_ids) + 1

    # check if addowner works with a valid user but invalid channel id
    data_addowner = json.dumps({
        "token": token_owner,
        "channel_id": invalid_channel_id,
        "u_id": u_id_non_owner
    }).encode('utf-8')
    req_addowner = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_addowner)

def test_channel_addowner_already_owner(auth_http_fixture):
    '''
    Test case when user is already an owner of the channel
    '''
    auth_fixture = auth_http_fixture
    # user1 and create a channel (user1 will be owner of channel)
    token1 = auth_fixture[1]['token']
    u_id1 = auth_fixture[1]['u_id']
    u_id2 = auth_fixture[2]['u_id']

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

    # user1 adds user2 to public channel as owner
    data_addowner1 = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_addowner1 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner1, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addowner1)

    # user1 adds user2 to private channel as owner
    data_addowner2 = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_addowner2 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_addowner2, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_addowner2)

    # check for adding owner again 
    # user1 adds user2 to pub channel as owner again
    data_testadd1 = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_testadd1 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_testadd1, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_testadd1)

    # user1 adds user2 to priv channel as owner again
    data_testadd2 = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_testadd2 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_testadd2, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_testadd2)

    # check for adding owner when they are already an owner
    # user1 adds user1 to pub channel as owner
    data_testadd3 = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id1
    }).encode('utf-8')
    req_testadd3 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_testadd3, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_testadd3)

    # user1 adds user1 to priv channel as owner
    data_testadd4 = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id1
    }).encode('utf-8')
    req_testadd4 = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_testadd4, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_testadd4)

def test_channel_addowner_user_not_channel_owner(auth_http_fixture):
    '''
    Test case when authorised user is not an owner of the channel or not an owner of slack
    '''
    auth_fixture = auth_http_fixture

    # get user data
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    u_id2 = auth_fixture[2]['u_id']
    u_id3 = auth_fixture[3]['u_id']

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

    # user1 invites user2 and user3 to join channels
    # invite user2 as member
    data_2invitepub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_2invitepub = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_2invitepub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_2invitepub)

    data_2invitepriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_2invitepriv = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_2invitepriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_2invitepriv)

    # invite user3 as member
    data_3invitepub = json.dumps({
        "token": token1,
        "channel_id": pub_channel_id,
        "u_id": u_id3
    }).encode('utf-8')
    req_3invitepub = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_3invitepub, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_3invitepub)

    data_3invitepriv = json.dumps({
        "token": token1,
        "channel_id": priv_channel_id,
        "u_id": u_id3
    }).encode('utf-8')
    req_3invitepriv = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_3invitepriv, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_3invitepriv)


    # user2 (non slack or channel owner) tries to add user3 as an owner
    # user 2 adds user3 to public channel as an owner
    data_2invite3pub = json.dumps({
        "token": token2,
        "channel_id": pub_channel_id,
        "u_id": u_id3
    }).encode('utf-8')
    req_2invite3pub = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_2invite3pub, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_2invite3pub)

    # user 2 adds user3 to private channel as an owner
    data_2invite3priv = json.dumps({
        "token": token2,
        "channel_id": priv_channel_id,
        "u_id": u_id3
    }).encode('utf-8')
    req_2invite3priv = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_2invite3priv, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_2invite3priv)

def test_channel_addowner_invalid_token(auth_http_fixture):
    '''
    Test case for invalid token
    '''
    auth_fixture = auth_http_fixture
    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']
    u_id2 = auth_fixture[2]['u_id']
    
    # set an invalid token 
    invalid_token = '12345'

    # user1 creates channel 
    data_create = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_create, method='POST', headers={"Content-Type": "application/json"})
    response_channel = urllib.request.urlopen(req)
    channel = json.load(response_channel)
    channel_id = channel['channel_id']

    # user1 trys to add user2 as owner with invalid token
    data_invalid = json.dumps({
        "token": invalid_token,
        "channel_id": channel_id,
        "u_id": u_id2
    }).encode('utf-8')
    req_invalid = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data_invalid, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_invalid)
