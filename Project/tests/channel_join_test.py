#pylint: disable=R0801
'''
Test file for function channel_join
Function specifications
- Given a channel_id of a channel that the authorised user can join, adds them to that channel
When testing this function, we assume that all other functions work as expected
'''
#pylint: disable=trailing-whitespace
#pylint: disable=line-too-long
#pylint: disable=unused-variable

import pytest
from error import InputError, AccessError
from channels import channels_create, channels_listall, channels_list
from channel import channel_join


def test_channel_join(channels_fixture):
    '''
    Test case for a simple channel join
    - channel will need to be created before running
    Assumption: 
        user has been created to not be a member of the channel
        channel is public 
    '''
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[0]["channels"][1]["channel_id"]
    channel_join(server_data, token, channel_id)

    # make sure channel exists in the list of users channels (if none can be found it means join did not work)
    channel_list_user1 = channels_list(server_data, token)['channels']
    assert any(True for i in channel_list_user1 if i['channel_id'] == channel_id) 

def test_channel_join_invalid_channel_id(channels_fixture):
    '''
    Test case for invalid channel ID
    - channel does not exist
    '''
    (server_data, channels_fixture) = channels_fixture

    # set invalid channel_id
    token = channels_fixture[1]["token"]
    all_channels = channels_listall(server_data, token)

    # as defined in data types where all variables with suffix _id will be an integer
    channel_ids = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_ids) + 1

    with pytest.raises(InputError) as error_raise:
        channel_join(server_data, token, invalid_channel_id)

def test_channel_join_double(channels_fixture):
    '''
    Test case for invalid channel ID
    - user is already part of the channel
    '''
    (server_data, channels_fixture) = channels_fixture

    # store channel id for a channel which the user is already a member of 
    token = channels_fixture[1]['token']
    dup_channel_id = channels_fixture[1]['channels'][0]['channel_id']

    with pytest.raises(AccessError) as error_raise:
        channel_join(server_data, token, dup_channel_id)

def test_channel_join_private_non_admin(auth_fixture):
    '''
    Test case for private channel
    - user is not admin (default slack member)
    '''
    (server_data, auth_fixture) = auth_fixture

    # Create private channel with a user then see if another user (not admin) can join
    token1 = auth_fixture[1]['token']  
    token2 = auth_fixture[2]['token']  
    priv_channel_id = channels_create(server_data, token1, 'Private Channel', False)['channel_id']

    with pytest.raises(AccessError) as error_raise:
        channel_join(server_data, token2, priv_channel_id)

def test_channel_join_private_admin(auth_fixture):
    '''
    Test case for private channel
    - user is admin (slackrowner)
    '''
    (server_data, auth_fixture) = auth_fixture

    # store user data for slackrowner and normal user
    slackrtoken = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']  
    
    # Create private channel with a user1 then see if slackrowner can join
    priv_channel_id = channels_create(server_data, token1, 'Private Channel', False)['channel_id']
    channel_join(server_data, slackrtoken, priv_channel_id)
    
    # make sure channel exists in the list of slackrowners channels (if none can be found it means join did not work)
    channel_list_slackrowner = channels_list(server_data, slackrtoken)['channels']
    assert any(True for i in channel_list_slackrowner if i['channel_id'] == priv_channel_id)     

def test_channel_join_invalid_token(auth_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, auth_fixture) = auth_fixture

    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']

    # set an invalid token 
    invalid_token = '12345'

    # user1 creates channel 
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    
    with pytest.raises(AccessError) as error_raise:
        channel_join(server_data, invalid_token, channel_id)
