#pylint: disable=R0801
'''
Test file for function channel_leave
When testing this function, we assume that all other functions work as expected
'''
#pylint: disable=trailing-whitespace
#pylint: disable=line-too-long
#pylint: disable=unused-variable
import pytest
from error import InputError, AccessError
from channels import channels_list, channels_listall, channels_create
from channel import channel_leave, channel_invite

def test_channel_leave(channels_fixture):
    '''
    Test case for a simple channel leave
    - user should not be in the list for that channel after they leave
    '''
    (server_data, channels_fixture) = channels_fixture
 
    # get user and channel details
    token = channels_fixture[1]['token']
    channel_id = channels_fixture[1]['channels'][0]['channel_id']

    # leave channel
    channel_leave(server_data, token, channel_id)

    # now check whether in the list of channels for that user the removed channel exists
    list_channels = channels_list(server_data, token)['channels']

    assert not any(True for x in list_channels if x['channel_id'] == channel_id)

def test_channel_leave_invalid_channel_id(channels_fixture):
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
        channel_leave(server_data, token, invalid_channel_id)

def test_channel_leave_not_member(channels_fixture):
    '''
    Test case for when user is not part of channel
    '''
    (server_data, channels_fixture) = channels_fixture      
    # store channel id for a channel which the user is not a member of 
    token1 = channels_fixture[1]['token']
    token2 = channels_fixture[2]['token']

    new_channel_id = channels_create(server_data, token1, 'New Channel', True)['channel_id']
    new_priv_channel_id = channels_create(server_data, token1, 'New Private Channel', False)['channel_id']
    
    with pytest.raises(AccessError) as error_raise:
        channel_leave(server_data, token2, new_channel_id)

    with pytest.raises(AccessError) as error_raise:
        channel_leave(server_data, token2, new_priv_channel_id)

def test_channel_leave_invalid_token(auth_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, auth_fixture) = auth_fixture    
    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']
    uid2 = auth_fixture[2]['u_id']

    # set an invalid token 
    invalid_token = '12345'

    # user1 creates channel 
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    channel_invite(server_data, token1, channel_id, uid2)

    # user2 tries to leave with invalid token
    with pytest.raises(AccessError) as error_raise:
        channel_leave(server_data, invalid_token, channel_id)
