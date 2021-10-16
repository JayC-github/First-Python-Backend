#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the message_edit function
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
#pylint: disable=too-many-locals
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_message_edit(auth_http_fixture):
    '''
    Test case for a simple message edit
    - authorised user has sent the message or authorised user is an admin or owner of the channel or slack
    '''
    auth_fixture = auth_http_fixture

    # get user details
    slckrtoken = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

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

    # user2 edits own message
    data_edit1 = json.dumps({
        "token": token2,
        "message_id": msg1,
        "message": 'I can edit my own message'
    }).encode('utf-8')
    req_edit1 = urllib.request.Request(f"{BASE_URL}/message/edit", data=data_edit1, method='PUT', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_edit1)

    # user1 (owner of channel where message was sent) edits message of user2
    data_edit2 = json.dumps({
        "token": token1,
        "message_id": msg2,
        "message": 'I can edit as a channel owner!'
    }).encode('utf-8')
    req_edit2 = urllib.request.Request(f"{BASE_URL}/message/edit", data=data_edit2, method='PUT', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_edit2)

    # slackr owner edits message of user2
    data_edit3 = json.dumps({
        "token": slckrtoken,
        "message_id": msg3,
        "message": 'I can edit whatever I want!!!'
    }).encode('utf-8')
    req_edit3 = urllib.request.Request(f"{BASE_URL}/message/edit", data=data_edit3, method='PUT', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_edit3)

    # get all messages for user2
    query_str = 'I+can+edit+'
    response_check = urllib.request.urlopen(f"{BASE_URL}/search?token={token2}&query_str={query_str}")
    payload_check = json.load(response_check)
    msg_list = payload_check['messages']

    msg1edit = [i['message'] for i in msg_list if i['message_id'] == msg1]    
    msg2edit = [i['message'] for i in msg_list if i['message_id'] == msg2]    
    msg3edit = [i['message'] for i in msg_list if i['message_id'] == msg3]  
  
    # checks if the message contents have been changed
    assert msg1edit == ['I can edit my own message']
    assert msg2edit == ['I can edit as a channel owner!']
    assert msg3edit == ['I can edit whatever I want!!!']

def test_message_edit_empty_string(auth_http_fixture):
    '''
    Test case for a message edit with empty string
    '''
    auth_fixture = auth_http_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    
    # create channels
    data_pub = json.dumps({
        "token": token1,
        "name": "A Public Channel",
        "is_public": True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data_pub, method='POST', headers={"Content-Type": "application/json"})
    response_pub = urllib.request.urlopen(req)
    pub_channel = json.load(response_pub)
    channel_id = pub_channel['channel_id']

    # user1 sends message to channel
    data_send = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "message": 'Hello there I am a user'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msg1 = payload_send["message_id"]

    # user1 edits own message with empty string
    data_edit = json.dumps({
        "token": token1,
        "message_id": msg1,
        "message": ''
    }).encode('utf-8')
    req_edit = urllib.request.Request(f"{BASE_URL}/message/edit", data=data_edit, method='PUT', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_edit)

    # find the message
    response_check = urllib.request.urlopen(f"{BASE_URL}/search?token={token1}&query_str=")
    payload_check = json.load(response_check)
    msg_list = payload_check['messages']

    msg1edit = [i['message'] for i in msg_list if i['message_id'] == msg1]  

    # make sure message doesnt exists
    assert msg1edit == []


def test_message_edit_invalid_access(auth_http_fixture):
    '''
    Test case when the authorised user does not have the necessary access to edit the message
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

    # user1 sends message to channel
    data_send = json.dumps({
        "token": token1,
        "channel_id": channel_id,
        "message": 'User 2 does not have access to edit this!'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msg1 = payload_send["message_id"]

    # check if user2 can edit this message (if so then raise Access Error)
    data_edit = json.dumps({
        "token": token2,
        "message_id": msg1,
        "message": 'I WANT TO CHANGE THIS'
    }).encode('utf-8')
    req_edit = urllib.request.Request(f"{BASE_URL}/message/edit", data=data_edit, method='PUT', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_edit)

def test_message_edit_invalid_token(auth_http_fixture):
    '''
    Test case for invalid token
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

    # check if user2 can edit this message (if so then raise Access Error)
    data_edit = json.dumps({
        "token": invalidtoken,
        "message_id": msg1,
        "message": 'INVALID TOKEN SHOULDNT WORK'
    }).encode('utf-8')
    req_edit = urllib.request.Request(f"{BASE_URL}/message/edit", data=data_edit, method='PUT', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_edit)
