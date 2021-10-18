#pylint: disable=R0801
'''
Test file for function message_pin and message_unpin
When testing this function, we assume that all other functions work as expected
Needs to be run after all imported functions are tested
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
import pytest
from error import InputError, AccessError
from message import message_send, message_pin, message_unpin
from channel import channel_invite
from search import search

def test_message_pin_upin(channels_fixture):
    '''
    Test case for working pin and unpin feature 
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    
    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Pin and unpin this')['message_id']

    # pin the message
    message_pin(server_data, token, msgid)

    # make sure that the message is pinned
    msg_list1 = search(server_data, token, 'Pin and unpin this')['messages']
    msgpin = [i['is_pinned'] for i in msg_list1 if i['message_id'] == msgid]   
    assert msgpin == [True]
    
    # unpin the message 
    message_unpin(server_data, token, msgid)

    #m make sure that the message is unpinned
    msg_list2 = search(server_data, token, 'Pin and unpin this')['messages']
    msgunpin = [i['is_pinned'] for i in msg_list2 if i['message_id'] == msgid]   
    assert msgunpin == [False]

def test_message_pin_invalid_msg_id(channels_fixture):
    '''
    Test case for invalid message_id
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalid_message_id = -1

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Invalid message ID')['message_id']

    # try to pin the message
    with pytest.raises(InputError) as error_raise:
        message_pin(server_data, token, invalid_message_id)

def test_message_pin_non_owner(channels_fixture):
    '''
    Test case for when non owner of a channel tries to pin a message
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token1 = channels_fixture[1]["token"]
    token2 = channels_fixture[2]["token"]
    uid2 = channels_fixture[2]["u_id"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # user1 invites user2 to channel1
    channel_invite(server_data, token1, channel_id, uid2)

    # user1 sends a message to channel 1
    msgid = message_send(server_data, token1, channel_id, 'Only owners can pin')['message_id']

    # try to pin the message
    with pytest.raises(InputError) as error_raise:
        message_pin(server_data, token2, msgid)

def test_message_pin_already_pinned(channels_fixture):
    '''
    Test case for duplicate pin
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Duplicate pin')['message_id']

    # pin the message    
    message_pin(server_data, token, msgid)

    # try to pin the message again
    with pytest.raises(InputError) as error_raise:
        message_pin(server_data, token, msgid)

def test_message_pin_non_member(channels_fixture):
    '''
    Test case for non member trying to pin
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token1 = channels_fixture[1]["token"]
    token2 = channels_fixture[2]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # user1 sends a message to channel 1
    msgid = message_send(server_data, token1, channel_id, 'Members cant pin can pin')['message_id']

    # try to pin the message with user2 (non member of channel1)
    with pytest.raises(AccessError) as error_raise:
        message_pin(server_data, token2, msgid)

def test_message_pin_invalid_token(channels_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalidtoken = '12345'
    # user1 sends a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Members cant pin can pin')['message_id']

    # try to pin the message with invalid
    with pytest.raises(AccessError) as error_raise:
        message_pin(server_data, invalidtoken, msgid)

def test_message_unpin_invalid_msg_id(channels_fixture):
    '''
    Test case for invalid message_id
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalid_message_id = -1

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Invalid message ID')['message_id']
    
    # pin the message 
    message_pin(server_data, token, msgid)

    # try to unpin the message
    with pytest.raises(InputError) as error_raise:
        message_unpin(server_data, token, invalid_message_id)

def test_message_unpin_non_owner(channels_fixture):
    '''
    Test case for when non owner of a channel tries to unpin a message
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token1 = channels_fixture[1]["token"]
    token2 = channels_fixture[2]["token"]
    uid2 = channels_fixture[2]["u_id"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # user1 invites user2 to channel1
    channel_invite(server_data, token1, channel_id, uid2)

    # user1 sends a message to channel 1
    msgid = message_send(server_data, token1, channel_id, 'Only owners can pin')['message_id']

    # user1 pins the message 
    message_pin(server_data, token1, msgid)

    # try to pin the message
    with pytest.raises(InputError) as error_raise:
        message_unpin(server_data, token2, msgid)

def test_message_unpin_already_pinned(channels_fixture):
    '''
    Test case for duplicate unpin
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # send a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Duplicate unpin')['message_id']

    # pin the message    
    message_pin(server_data, token, msgid)

    # unpin the message
    message_unpin(server_data, token, msgid)

    # try to unpin the message again
    with pytest.raises(InputError) as error_raise:
        message_unpin(server_data, token, msgid)


def test_message_unpin_non_member(channels_fixture):
    '''
    Test case for non member trying to pin
    '''
    (server_data, channels_fixture) = channels_fixture

    # get details for user1 and channel 1
    token1 = channels_fixture[1]["token"]
    token2 = channels_fixture[2]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]

    # user1 sends a message to channel 1
    msgid = message_send(server_data, token1, channel_id, 'Members cant pin can pin')['message_id']

    # pin the message    
    message_pin(server_data, token1, msgid)

    # try to unpin the message with user2 (non member of channel1)
    with pytest.raises(AccessError) as error_raise:
        message_unpin(server_data, token2, msgid)

def test_message_unpin_invalid_token(channels_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[1]["channels"][0]["channel_id"]
    invalidtoken = '12345'
    # user1 sends a message to channel 1
    msgid = message_send(server_data, token, channel_id, 'Members cant pin can pin')['message_id']

    # pin the message    
    message_pin(server_data, token, msgid)

    # try to unpin the message with invalid token
    with pytest.raises(AccessError) as error_raise:
        message_unpin(server_data, invalidtoken, msgid)
