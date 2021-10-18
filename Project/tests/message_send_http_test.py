#pylint: disable=R0801
'''
Test file for server server.py
This file run http testing for the message_send function
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_message_send(channels_http_fixture):
    '''
    Tests message send functionality
    '''
    channels_fixture = channels_http_fixture

    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    message_content = "Hello, I am richard"

    # Needs to have server data set before running this 
    jsondata_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": message_content
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=jsondata_send, method='POST', headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload_send = json.load(response)
    message_id = payload_send["message_id"]

    # check if the return contains the correct type
    assert isinstance(message_id, int)
    message_content_http = "Hello,+I+am+richard"
    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token}&query_str={message_content_http}")
    payload_search = json.load(response)

    #Check if message search finds the message and it has the appropriate ID and contents
    assert [msg["message"] for msg in payload_search["messages"] if msg["message_id"] == message_id] == [message_content]

def test_message_send_long(channels_http_fixture):
    '''
    Test for when message is longer than 1000 characters
    '''
    channels_fixture = channels_http_fixture
    token = channels_fixture[0]["token"]
    channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    test_msg = "a"*2000

    data_send = json.dumps({
        "token": token,
        "channel_id": channel_id,
        "message": test_msg
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})

    #sending a msg longer than 1000 characters
    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req)

def test_invalid_token(channels_http_fixture):
    '''
    Testing invalid Token
    '''
    channels_fixture = channels_http_fixture

    invalid_token = "12345"
    user_channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    normal_msg = "Steven is cool"

    data_send = json.dumps({
        "token": invalid_token,
        "channel_id": user_channel_id,
        "message": normal_msg
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data_send, method='POST', headers={"Content-Type": "application/json"})

    #messaging with a invalid token
    with pytest.raises(urllib.error.HTTPError) as error_raise:
        urllib.request.urlopen(req)
