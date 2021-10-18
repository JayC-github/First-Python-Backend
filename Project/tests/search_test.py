#pylint: disable=C0301,W0106, R0914
#pylint: disable=R0801
'''
Test file for function search
When testing this function, we assume that all other functions work as expected

Needs to be run after all imported functions are tested
'''

import pytest
from error import AccessError
from channels import channels_create
from channel import channel_invite
from message import message_send
from search import search

def test_search_working(auth_fixture):
    '''
    Test case for a working search case
    '''
    (server_data, auth_fixture) = auth_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channel
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    channel_invite(server_data, token1, channel_id, uid2)

    # send messages in the channel
    msg1 = message_send(server_data, token1, channel_id, 'TEST is good!')['message_id']
    msg2 = message_send(server_data, token2, channel_id, 'TEST is mad!')['message_id']

    # make sure search shows correct list of messages
    msglist1 = search(server_data, token1, 'TEST is ')['messages']
    msglist2 = search(server_data, token2, 'TEST is ')['messages']

    assert [i['message_id'] for i in msglist1 if i['message_id'] in (msg1, msg2)] == [msg2, msg1]
    assert [i['message_id'] for i in msglist2 if i['message_id'] in (msg1, msg2)] == [msg2, msg1]


def test_search_messages_multiple_chnl(auth_fixture):
    '''
    Test case for messages in multiple channels
    '''
    (server_data, auth_fixture) = auth_fixture
   # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    token3 = auth_fixture[3]['token']
    token4 = auth_fixture[4]['token']
    uid2 = auth_fixture[2]['u_id']
    uid4 = auth_fixture[4]['u_id']

    # create channel and invite members (pub channel: user1 user2, priv channel: user2 user3 user4)
    pubid = channels_create(server_data, token1, 'Pub_Channel', True)['channel_id']
    privid = channels_create(server_data, token3, 'Priv_Channel', True)['channel_id']
    channel_invite(server_data, token1, pubid, uid2)
    channel_invite(server_data, token3, privid, uid2)
    channel_invite(server_data, token3, privid, uid4)

    # send messages in the channel
    msg1 = message_send(server_data, token1, pubid, 'User1 is good!')['message_id']
    msg2 = message_send(server_data, token2, pubid, 'User2 is good!')['message_id']
    msg3 = message_send(server_data, token2, privid, 'User2 is bad!')['message_id']
    msg4 = message_send(server_data, token3, privid, 'User3 is good!')['message_id']
    msg5 = message_send(server_data, token4, privid, 'User4 is good!')['message_id']

    # make sure search shows correct list of messages
    msglist1 = search(server_data, token1, 'User')['messages']
    msglist2 = search(server_data, token2, 'User')['messages']
    msglist3 = search(server_data, token3, 'User')['messages']
    msglist4 = search(server_data, token4, 'User')['messages']

    assert [i['message_id'] for i in msglist1 if i['message_id'] in (msg1, msg2)] == [msg2, msg1]
    assert [i['message_id'] for i in msglist2 if i['message_id'] in (msg1, msg2, msg3, msg4, msg5)] == [msg5, msg4, msg3, msg2, msg1]
    assert [i['message_id'] for i in msglist3 if i['message_id'] in (msg3, msg4, msg5)] == [msg5, msg4, msg3]
    assert [i['message_id'] for i in msglist4 if i['message_id'] in (msg3, msg4, msg5)] == [msg5, msg4, msg3]

def test_search_empty_query(auth_fixture):
    '''
    Test case for empty query
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    token1 = auth_fixture[1]['token']

    # create channel
    channel_id1 = channels_create(server_data, token1, 'New Channel', True)['channel_id']
    channel_id2 = channels_create(server_data, token1, 'New Channel1', True)['channel_id']

    # send messages in the channel
    msg1 = message_send(server_data, token1, channel_id1, 'User1 is good!')['message_id']
    msg2 = message_send(server_data, token1, channel_id1, 'User1 is goooooooooood!')['message_id']
    msg3 = message_send(server_data, token1, channel_id1, 'All messages should pop up@')['message_id']
    msg4 = message_send(server_data, token1, channel_id2, 'User1 is good!')['message_id']
    msg5 = message_send(server_data, token1, channel_id2, 'User1 is goooooooooood!')['message_id']
    msg6 = message_send(server_data, token1, channel_id2, 'All messages should pop up@')['message_id']

    # make sure search shows all messages for the user if query is blank string
    msglist1 = search(server_data, token1, '')['messages']

    assert [i['message_id'] for i in msglist1] == [msg6, msg5, msg4, msg3, msg2, msg1]

def test_search_empty_msg_list(auth_fixture):
    '''
    Test case for empty message list
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']

    # create channels
    channel_id1 = channels_create(server_data, token1, 'New Channel', True)['channel_id']
    channels_create(server_data, token2, 'Another Channel', True)['channel_id']

    # make sure search shows no messages
    msglist1 = search(server_data, token2, '')['messages']

    assert [i['message_id'] for i in msglist1] == []

    # send messages with user1 on channel1
    message_send(server_data, token1, channel_id1, 'User1 only!')['message_id']

    # make sure search still shows no messages for user2
    msglist2 = search(server_data, token2, '')['messages']

    assert [i['message_id'] for i in msglist2] == []

def test_search_invalid_token(auth_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    token1 = auth_fixture[1]['token']
    invalidtoken = '12345'

    # create channels
    channels_create(server_data, token1, 'New Channel', True)['channel_id']

    with pytest.raises(AccessError):
        search(server_data, invalidtoken, '')
