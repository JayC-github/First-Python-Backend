#pylint: disable=R0801
'''
Test file for function message_react and message_unreact
When testing this function, we assume that all other functions work as expected
Needs to be run after all imported functions are tested
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
import pytest
from error import InputError, AccessError
from message import message_send, message_react, message_unreact
from search import search

def test_message_react_unreact(channels_fixture):
    '''
    Test case for working react and unreact feature 
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    uid = channels_fixture[1]["u_id"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'react and unreact this')['message_id']

    # react to the message
    message_react(server_data, token, msgid, 1)

    # make sure that the message has a react
    msg_list1 = search(server_data, token, 'react and unreact this')['messages']
    msgreacts = next(i['reacts'] for i in msg_list1 if i['message_id'] == msgid)
    msgreact_uids = next(i['u_ids'] for i in msgreacts if i['react_id'] == 1)

    # make sure react with react_id 1 exists 
    assert any(msgreact_uids)

    # make sure react has been done by user1
    assert any(True for i in msgreact_uids if i == uid)
  
    # unreact the message 
    message_unreact(server_data, token, msgid, 1)

    # make sure that the message has no react for user1
    msg_list2 = search(server_data, token, 'react and unreact this')['messages']
    msgununreacts = next(i['reacts'] for i in msg_list2 if i['message_id'] == msgid)
    msgununreacts_uids = next(i['u_ids'] for i in msgununreacts if i['react_id'] == 1)

    assert not any(True for i in msgununreacts_uids if i == uid)

def test_message_react_invalid_msgid(channels_fixture):
    '''
    Test case for when message_id is not a valid message within a channel that the authorised user has joined
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalid_message_id = -1

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'invalid msg id')['message_id']

    # try to react to the message
    with pytest.raises(InputError) as error_raise:
        message_react(server_data, token, invalid_message_id, 1)

def test_message_react_invalid_react(channels_fixture):
    '''
    Test case for when react_id is not a valid React ID
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'invalid react id')['message_id']

    # try to react to the message
    with pytest.raises(InputError) as error_raise:
        message_react(server_data, token, msgid, 2)

def test_message_react_not_active(channels_fixture):
    '''
    Test case for when Message with ID message_id already contains an active React with ID react_id
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'react already active')['message_id']

    # react to the message
    message_react(server_data, token, msgid, 1)

    # react again
    with pytest.raises(InputError) as error_raise:
        message_react(server_data, token, msgid, 1)


def test_message_react_invalid_token(channels_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    invalid_token = '12345'
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'invalid token')['message_id']

    # try to react to the message
    with pytest.raises(AccessError) as error_raise:
        message_react(server_data, invalid_token, msgid, 1)

def test_message_unreact_invalid_msgid(channels_fixture):
    '''
    Test case for when message_id is not a valid message within a channel that the authorised user has joined
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalid_message_id = -1

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'invalid msg id')['message_id']

    # react to the message
    message_react(server_data, token, msgid, 1)

    # try to unreact
    with pytest.raises(InputError) as error_raise:
        message_unreact(server_data, token, invalid_message_id, 1)

def test_message_unreact_invalid_react(channels_fixture):
    '''
    Test case for when react_id is not a valid React ID
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'invalid react id')['message_id']

    # try to unreact
    with pytest.raises(InputError) as error_raise:
        message_unreact(server_data, token, msgid, 2)

def test_message_unreact_not_active(channels_fixture):
    '''
    Test case for when Message with ID message_id already contains an active React with ID react_id
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'react not active')['message_id']

    # react to the message
    message_react(server_data, token, msgid, 1)

    # unreacts
    message_unreact(server_data, token, msgid, 1)

    # try to unreact again
    with pytest.raises(InputError) as error_raise:
        message_unreact(server_data, token, msgid, 1)

def test_message_unreact_invalid_token(channels_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    invalid_token = '12345'
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'invalid token')['message_id']

    # react to the message
    message_react(server_data, token, msgid, 1)
    
    with pytest.raises(AccessError) as error_raise:
        message_unreact(server_data, invalid_token, msgid, 1)
