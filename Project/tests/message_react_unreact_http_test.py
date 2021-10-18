#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the message_react and message_unreact function
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

def test_message_react_unreact(channels_http_fixture):
    '''
    Test case for working react and unreact feature 
    '''
    channels_fixture = channels_http_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    uid = channels_fixture[1]["u_id"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    data_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": 'react and unreact this'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msgid = payload_send["message_id"]

    # react to the message
    data_react = json.dumps({
        "token": token,
        "message_id": msgid,
        "react_id": 1
    }).encode('utf-8')
    req_react = urllib.request.Request(f"{BASE_URL}/message/react", data=data_react, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_react)

    # make sure that the message has a react
    response_check = urllib.request.urlopen(f"{BASE_URL}/search?token={token}&query_str=react+and+unreact+this")
    payload_check = json.load(response_check)
    msg_list1 = payload_check['messages']
    msgreacts = next(i['reacts'] for i in msg_list1 if i['message_id'] == msgid)
    msgreact_uids = next(i['u_ids'] for i in msgreacts if i['react_id'] == 1)

    # make sure react with react_id 1 exists 
    assert any(msgreact_uids)

    # make sure react has been done by user1
    assert any(True for i in msgreact_uids if i == uid)
  
    # unreact the message 
    data_unreact = json.dumps({
        "token": token,
        "message_id": msgid,
        "react_id": 1
    }).encode('utf-8')
    req_unreact = urllib.request.Request(f"{BASE_URL}/message/unreact", data=data_unreact, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_unreact)

    # make sure no react has been done by user1
    response_check2 = urllib.request.urlopen(f"{BASE_URL}/search?token={token}&query_str=react+and+unreact+this")
    payload_check2 = json.load(response_check2)
    msg_list2 = payload_check2['messages']

    msgununreacts = next(i['reacts'] for i in msg_list2 if i['message_id'] == msgid)
    msgununreacts_uids = next(i['u_ids'] for i in msgununreacts if i['react_id'] == 1)

    assert not any(True for i in msgununreacts_uids if i == uid)

def test_message_react_invalid_token(channels_http_fixture):
    '''
    Test case for invalid token
    '''
    channels_fixture = channels_http_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    invalid_token = '12345'
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    data_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": 'invalid token'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msgid = payload_send["message_id"]

    # try to react to the message
    data_react = json.dumps({
        "token": invalid_token,
        "message_id": msgid,
        "react_id": 1
    }).encode('utf-8')
    req_react = urllib.request.Request(f"{BASE_URL}/message/react", data=data_react, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_react)

def test_message_unreact_invalid_token(channels_http_fixture):
    '''
    Test case for invalid token
    '''
    channels_fixture = channels_http_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    invalid_token = '12345'
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    data_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": 'invalid token'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msgid = payload_send["message_id"]

    # react to the message
    data_react = json.dumps({
        "token": token,
        "message_id": msgid,
        "react_id": 1
    }).encode('utf-8')
    req_react = urllib.request.Request(f"{BASE_URL}/message/react", data=data_react, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_react)
    
    # try to unreact with invalid token
    data_unreact = json.dumps({
        "token": invalid_token,
        "message_id": msgid,
        "react_id": 1
    }).encode('utf-8')
    req_unreact = urllib.request.Request(f"{BASE_URL}/message/unreact", data=data_unreact, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_unreact)
