#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the message_send function
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=too-many-locals
#pylint: disable=unused-variable
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_message_remove_simple(auth_http_fixture):
    '''
    Test case for a simple message remove
    - authorised user has sent the message or authorised user is an admin or owner of the channel or slack
    - message (based on ID exists)
    - user2 will send 3 messages
    - user2, slackrowner and channel owner will try to remove messages
    '''
    auth_fixture = auth_http_fixture

    # get user details
    slckrtoken = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channels and invite users
    # user1 creates a public channel 
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']
    
    # user1 invites user2 to the channel
    data_invite = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_invite = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invite, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invite)

    # user2 sends 3 messages to channel
    data_send1 = json.dumps({
        "token": token2,
        "channel_id": channel_id,
        "message": 'Hello there friend'
    }).encode('utf-8')
    req_send1 = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send1, method='POST', headers={"Content-Type": "application/json"})
    response_send1 = urllib.request.urlopen(req_send1)
    payload_send1 = json.load(response_send1)
    msg1 = payload_send1["message_id"]

    data_send2 = json.dumps({
        "token": token2,
        "channel_id": channel_id,
        "message": 'Hello there good friend!!'
    }).encode('utf-8')
    req_send2 = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send2, method='POST', headers={"Content-Type": "application/json"})
    response_send2 = urllib.request.urlopen(req_send2)
    payload_send2 = json.load(response_send2)
    msg2 = payload_send2["message_id"]

    data_send3 = json.dumps({
        "token": token2,
        "channel_id": channel_id,
        "message": 'Hello there bad friend :('
    }).encode('utf-8')
    req_send3 = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send3, method='POST', headers={"Content-Type": "application/json"})
    response_send3 = urllib.request.urlopen(req_send3)
    payload_send3 = json.load(response_send3)
    msg3 = payload_send3["message_id"]

    # user2 deletes own message
    data_rmv1 = json.dumps({
        "token": token2,
        "message_id": msg1
    }).encode('utf-8')
    req_rmv1 = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv1, method='DELETE', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_rmv1)

    # user1 (owner of channel where message was sent) deletes message of user2
    data_rmv2 = json.dumps({
        "token": token1,
        "message_id": msg2
    }).encode('utf-8')
    req_rmv2 = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv2, method='DELETE', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_rmv2)

    # slackr owner deletes message of user2
    data_rmv3 = json.dumps({
        "token": slckrtoken,
        "message_id": msg3
    }).encode('utf-8')
    req_rmv3 = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv3, method='DELETE', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_rmv3)

    # get all messages for user2
    response_check = urllib.request.urlopen(f"{BASE_URL}/search?token={token2}&query_str=Hello+there+")
    payload_check = json.load(response_check)
    msg_list = payload_check['messages']

    # checks if any exist in the list (if even 1 exists then function has failed)
    assert not any(True for i in msg_list if i['message_id'] in (msg1, msg2, msg3))

def test_message_remove_invalid_input(auth_http_fixture):
    '''
    Test case when message doesnt exist 
    - message (based on ID) no longer exists as it was already removed
    '''
    auth_fixture = auth_http_fixture

    # get user details 
    token1 = auth_fixture[1]['token']

    # create channel and send message to channel
    # create channel with user1
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']

    # send message with user1
    data_send1 = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "message": 'Just checking invalid messages'
    }).encode('utf-8')
    req_send1 = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send1, method='POST', headers={"Content-Type": "application/json"})
    response_send1 = urllib.request.urlopen(req_send1)
    payload_send1 = json.load(response_send1)
    msg1 = payload_send1["message_id"]

    # remove the message 
    data_rmv1 = json.dumps({
        "token": token1,
        "message_id": msg1
    }).encode('utf-8')
    req_rmv1 = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv1, method='DELETE', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_rmv1)

    # try removing the message again
    data_rmv2 = json.dumps({
        "token": token1,
        "message_id": msg1
    }).encode('utf-8')
    req_rmv2 = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv2, method='DELETE', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmv2)

def test_message_remove_invalid_access(auth_http_fixture):
    '''
    Test case when the authorised user does not have the necessary access to remove the message
    - message was not sent by authorised user and authorised user is not an admin or owner of the channel or slack
    '''
    auth_fixture = auth_http_fixture

    # get user details where user2 will not send the message and will not be an owner (slackr or channel)
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']
    
    # create channel with user1 and invite user2
    # user1 creates a public channel 
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']
    
    # user1 invites user2 to the channel
    data_invite = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "u_id": uid2
    }).encode('utf-8')
    req_invite = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data_invite, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_invite)

    # send message with user1
    data_send = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "message": 'User 2 does not have access to delete this!'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msg1 = payload_send["message_id"]

    # check if user2 can delete this message (if so then raise Access Error)
    data_rmv = json.dumps({
        "token": token2,
        "message_id": msg1
    }).encode('utf-8')
    req_rmv = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv, method='DELETE', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmv)

def test_message_remove_invalid_token(auth_http_fixture):
    '''
    Test case when token is invalid
    '''
    auth_fixture = auth_http_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    invalidtoken = '12345'

    # user1 creates a public channel 
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']

    # send message with user1
    data_send = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "message": 'User 2 does not have access to delete this!'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msg1 = payload_send["message_id"]

    # remove the message with an invalid token
    data_rmv = json.dumps({
        "token": invalidtoken,
        "message_id": msg1
    }).encode('utf-8')
    req_rmv = urllib.request.Request(f"{BASE_URL}/message/remove", data=data_rmv, method='DELETE', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_rmv)
