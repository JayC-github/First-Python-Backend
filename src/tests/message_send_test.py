#pylint: disable=R0801
'''
Test file for function message_send
When testing this function, we assume that all other functions work as expected
Needs to be run after all imported functions are tested
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
import pytest
from error import InputError, AccessError
from message import message_send
from search import search

def test_message_long_message(channels_fixture):
    '''
    Message is over 1000 words
    '''
    (server_data, channels_fixture) = channels_fixture
    usertoken = channels_fixture[0]["token"]
    user_channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    test_msg = "a"*2000
    
    #sending a msg longer than 1000 characters
    with pytest.raises(InputError) as error_raise:
        message_send(server_data, usertoken, user_channel_id, test_msg)

def test_message_hasnt_joined_channel(channels_fixture):
    '''
    Testing case when user has not joined channel
    '''
    (server_data, channels_fixture) = channels_fixture
    usertoken = channels_fixture[1]["token"]
    sender_channel_id = channels_fixture[2]["channels"][0]["channel_id"]
    normal_msg = "Steven is cool"
    
    #messaging with a differnt channel_id
    with pytest.raises(AccessError) as error_raise:
        message_send(server_data, usertoken, sender_channel_id, normal_msg)

def test_invalid_token(channels_fixture):
    '''
    Testing invalid Token
    '''
    (server_data, channels_fixture) = channels_fixture
    invalid_token = "12345"
    user_channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    normal_msg = "Steven is cool"
    
    #messaging with a invalid token
    with pytest.raises(AccessError) as error_raise:
        message_send(server_data, invalid_token, user_channel_id, normal_msg)

def test_message_in_channel(channels_fixture):
    '''
    Checking if message is in channel
    '''
    (server_data, channels_fixture) = channels_fixture
    usertoken = channels_fixture[0]["token"]
    user_channel_id = channels_fixture[0]["channels"][0]["channel_id"]
    normal_msg = "Steven is cool"

    #send msg
    msgid = message_send(server_data, usertoken, user_channel_id, normal_msg)['message_id']

    #check if its in the channel
    msgsearch = search(server_data, usertoken, "Steven is cool")["messages"]
        
    assert [i['message_id'] for i in msgsearch if i['message_id'] == msgid] == [msgid]
