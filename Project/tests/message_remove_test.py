#pylint: disable=R0801
'''
Test file for function message_edit
When testing this function, we assume that all other functions work as expected
Needs to be run after all imported functions are tested
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
import pytest
from error import InputError, AccessError
from channels import channels_create
from channel import channel_invite
from message import message_send, message_remove
from search import search

def test_message_remove_simple(auth_fixture):
    '''
    Test case for a simple message remove
    - authorised user has sent the message or authorised user is an admin or owner of the channel or slack
    - message (based on ID exists)
    '''
    (server_data, auth_fixture) = auth_fixture

    # get user details
    slckrtoken = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channels
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']  
    channel_invite(server_data, token1, channel_id, uid2)

    # user2 sends 3 messages to channel
    msg1 = message_send(server_data, token2, channel_id, 'Hello there friend')['message_id']
    msg2 = message_send(server_data, token2, channel_id, 'Hello there good friend!!')['message_id']
    msg3 = message_send(server_data, token2, channel_id, 'Hello there bad friend :(')['message_id']

    # user2 deletes own message
    message_remove(server_data, token2, msg1)

    # user1 (owner of channel where message was sent) deletes message of user2
    message_remove(server_data, token1, msg2)

    # slackr owner deletes message of user2
    message_remove(server_data, slckrtoken, msg3)

    # get all messages for user2
    msg_list = search(server_data, token2, 'Hello there ')['messages']

    # checks if any exist in the list (if even 1 exists then function has failed)
    assert not any(True for i in msg_list if i['message_id'] in (msg1, msg2, msg3))

def test_message_remove_invalid_input(auth_fixture):
    '''
    Test case when message doesnt exist 
    - message (based on ID) no longer exists)
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details 
    token1 = auth_fixture[1]['token']

    # create channel and send message to channel
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    msg1 = message_send(server_data, token1, channel_id, 'Just checking invalid messages')['message_id']
    
    # remove the message 
    message_remove(server_data, token1, msg1)

    # Input error should be raised if msg1 still exists
    with pytest.raises(InputError) as error_raise:
        message_remove(server_data, token1, msg1)

def test_message_remove_invalid_access(auth_fixture):
    '''
    Test case when the authorised user does not have the necessary access to remove the message
    - message was not sent by authorised user and authorised user is not an admin or owner of the channel or slack
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details where user2 will not send the message and will not be an owner (slackr or channel)
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']
    
    # create channel with user1 and invite user2
    channel_id = channels_create(server_data, token1, 'New Channel', True)['channel_id']
    channel_invite(server_data, token1, channel_id, uid2)

    # send msg with user1
    msg1 = message_send(server_data, token1, channel_id, 'User 2 does not have access to delete this!')['message_id']

    # check if user2 can delete this message (if so then raise Access Error)
    with pytest.raises(AccessError) as error_raise:
        message_remove(server_data, token2, msg1)

def test_message_remove_invalid_token(auth_fixture):
    '''
    Test case when token is invalid
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    token1 = auth_fixture[1]['token']
    invalidtoken = '12345'

    # create channel with user1
    channel_id = channels_create(server_data, token1, 'New Channel', True)['channel_id']

    # send msg with user1
    msg1 = message_send(server_data, token1, channel_id, 'Testing for invalid token!')['message_id']

    with pytest.raises(AccessError) as error_raise:
        message_remove(server_data, invalidtoken, msg1)
