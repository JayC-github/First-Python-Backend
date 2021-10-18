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
from error import AccessError, InputError
from channels import channels_create
from channel import channel_invite
from message import message_send, message_edit
from search import search

def test_message_edit(auth_fixture):
    '''
    Test case for a simple message edit
    - authorised user has sent the message or authorised user is an admin or owner of the channel or slack
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

    # user2 edits own message
    message_edit(server_data, token2, msg1, 'I can edit my own message')

    # user1 (owner of channel where message was sent) edits message of user2
    message_edit(server_data, token1, msg2, 'I can edit as a channel owner!')

    # slackr owner edits message of user2
    message_edit(server_data, slckrtoken, msg3, 'I can edit whatever I want!!!')

    # get all messages for user2
    msg_list = search(server_data, token2, 'I can edit ')['messages']
    msg1edit = [i['message'] for i in msg_list if i['message_id'] == msg1]    
    msg2edit = [i['message'] for i in msg_list if i['message_id'] == msg2]    
    msg3edit = [i['message'] for i in msg_list if i['message_id'] == msg3]  
  
    # checks if the message contents have been changed
    assert msg1edit == ['I can edit my own message']
    assert msg2edit == ['I can edit as a channel owner!']
    assert msg3edit == ['I can edit whatever I want!!!']

def test_message_edit_empty_string(auth_fixture):
    '''
    Test case for a message edit with empty string
    '''
    (server_data, auth_fixture) = auth_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    
    # create channels
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']

    # user1 sends message to channel
    msg1 = message_send(server_data, token1, channel_id, 'Hello there I am a user')['message_id']

    # user1 edits own message with empty string
    message_edit(server_data, token1, msg1, '')

    # find the message
    msg_list = search(server_data, token1, '')['messages']
    msg1edit = [i['message'] for i in msg_list if i['message_id'] == msg1]  

    # make sure message doesnt exist
    assert msg1edit == []


def test_message_edit_message_too_long(auth_fixture):
    '''
    Test case for a message edit with empty string
    '''
    (server_data, auth_fixture) = auth_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    
    # create channels
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']

    # user1 sends message to channel
    msg1 = message_send(server_data, token1, channel_id, 'Hello there I am a user')['message_id']

    # user1 edits own message with empty string
    with pytest.raises(InputError):
        message_edit(server_data, token1, msg1, 'a'*1001)



def test_message_edit_invalid_access(auth_fixture):
    '''
    Test case when the authorised user does not have the necessary access to edit the message
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
    msg1 = message_send(server_data, token1, channel_id, 'User 2 does not have access to edit this!')['message_id']

    # check if user2 can edit this message (if so then raise Access Error)
    with pytest.raises(AccessError) as error_raise:
        message_edit(server_data, token2, msg1, 'I WANT TO CHANGE THIS')


def test_message_edit_invalid_token(auth_fixture):
    '''
    Test case for invalid token
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
        message_edit(server_data, invalidtoken, msg1, 'INVALID TOKEN SHOULDNT WORK')
