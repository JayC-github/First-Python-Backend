#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the message_pin and message_unpin function
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

def test_message_pin_upin(channels_http_fixture):
    '''
    Test case for working pin and unpin feature 
    '''
    channels_fixture = channels_http_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    data_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": 'Pin and unpin this'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msgid = payload_send["message_id"]

    # pin the message
    data_pin = json.dumps({
        "token": token,
        "message_id": msgid
    }).encode('utf-8')
    req_pin = urllib.request.Request(f"{BASE_URL}/message/pin", data=data_pin, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_pin)

    # make sure that the message is pinned
    response_check = urllib.request.urlopen(f"{BASE_URL}/search?token={token}&query_str=Pin+and+unpin+this")
    payload_check = json.load(response_check)
    msg_list1 = payload_check['messages']

    msgpin = [i['is_pinned'] for i in msg_list1 if i['message_id'] == msgid]   
    assert msgpin == [True]
    
    # unpin the message 
    data_unpin = json.dumps({
        "token": token,
        "message_id": msgid
    }).encode('utf-8')
    req_unpin = urllib.request.Request(f"{BASE_URL}/message/unpin", data=data_unpin, method='POST', headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req_unpin)

    #m make sure that the message is unpinned
    response_check2 = urllib.request.urlopen(f"{BASE_URL}/search?token={token}&query_str=Pin+and+unpin+this")
    payload_check2 = json.load(response_check2)
    msg_list2 = payload_check2['messages']

    msgunpin = [i['is_pinned'] for i in msg_list2 if i['message_id'] == msgid]   
    assert msgunpin == [False]

def test_message_pin_invalid_token(channels_http_fixture):
    '''
    Test case for invalid token
    '''
    channels_fixture = channels_http_fixture
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalidtoken = '12345'

    # user1 sends a message to channel 1]
    data_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": 'Invalid token'
    }).encode('utf-8')
    req_send = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})
    response_send = urllib.request.urlopen(req_send)
    payload_send = json.load(response_send)
    msgid = payload_send["message_id"]

    # try to pin the message with invalid token
    data_pin = json.dumps({
        "token": invalidtoken,
        "message_id": msgid
    }).encode('utf-8')
    req_pin = urllib.request.Request(f"{BASE_URL}/message/pin", data=data_pin, method='POST', headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req_pin)
