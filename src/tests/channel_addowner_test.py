#pylint: disable=R0801
'''
Test file for function channel_addowner
When testing this function, we assume that all other functions work as expected
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable

import pytest
from error import InputError, AccessError
from channels import channels_create, channels_listall
from channel import channel_addowner, channel_invite, channel_details

def test_channel_addowner(auth_fixture):
    '''
    Test case for a simple channel addowner
    - owner adding non member or member of channel as owner
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user list
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    token3 = auth_fixture[3]['token']
    u_id2 = auth_fixture[2]['u_id']
    u_id3 = auth_fixture[3]['u_id']

    # create channels with 1 user (user 1 is owner)
    pub_channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    priv_channel_id = channels_create(server_data, token1, 'Priv_Channel', False)['channel_id']

    # add user2 as member
    channel_invite(server_data, token1, pub_channel_id, u_id2)
    channel_invite(server_data, token1, priv_channel_id, u_id2)

    # add user2 as owner (channel member -> channel owner)
    channel_addowner(server_data, token1, pub_channel_id, u_id2)
    channel_addowner(server_data, token1, priv_channel_id, u_id2)

    # add user3 as owner (channel non-member -> channel owner)
    channel_addowner(server_data, token1, pub_channel_id, u_id3)
    channel_addowner(server_data, token1, priv_channel_id, u_id3)

    # get details of channels
    user2_channel_det1 = channel_details(server_data, token2, pub_channel_id)['owner_members']
    user2_channel_det2 = channel_details(server_data, token2, priv_channel_id)['owner_members']
 
    user3_channel_det1 = channel_details(server_data, token3, pub_channel_id)['owner_members']
    user3_channel_det2 = channel_details(server_data, token3, priv_channel_id)['owner_members']

    # check that user2 and user3 are both owners for each channel
    assert any(True for i in user2_channel_det1 if i['u_id'] == u_id2)
    assert any(True for i in user2_channel_det2 if i['u_id'] == u_id2)
    assert any(True for i in user3_channel_det1 if i['u_id'] == u_id3)
    assert any(True for i in user3_channel_det2 if i['u_id'] == u_id3)

def test_channel_addowner_invalid_channel_id(channels_fixture):
    '''
    Test case for invalid channel ID 
    - channel id does not exist
    '''
    (server_data, channels_fixture) = channels_fixture
    # get user details
    token_owner = channels_fixture[1]["token"]
    u_id_non_owner = channels_fixture[2]["u_id"]
    all_channels = channels_listall(server_data, token_owner)

    # as defined in data types where all variables with suffix _id will be an integer
    channel_ids = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_ids) + 1

    # check if addowner works with a valid user but invalid channel id
    with pytest.raises(InputError) as error_raise:
        channel_addowner(server_data, token_owner, invalid_channel_id, u_id_non_owner)

def test_channel_addowner_already_owner(auth_fixture):
    '''
    Test case when user is already an owner of the channel
    '''
    (server_data, auth_fixture) = auth_fixture
    # user1 and create a channel (user1 will be owner of channel)
    token1 = auth_fixture[1]['token']
    u_id1 = auth_fixture[1]['u_id']
    u_id2 = auth_fixture[2]['u_id']

    # create channels with 1 user (user 1 is owner)
    pub_channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    priv_channel_id = channels_create(server_data, token1, 'Priv_Channel', False)['channel_id']

    # user1 adds user2 as owner 
    channel_addowner(server_data, token1, pub_channel_id, u_id2) 
    channel_addowner(server_data, token1, priv_channel_id, u_id2) 

    # user1 adds user 2 as owner again or when user1 tries to add user1 as owner (InputError should pop up)
    with pytest.raises(InputError) as error_raise:
        channel_addowner(server_data, token1, pub_channel_id, u_id2) 

    with pytest.raises(InputError) as error_raise:
        channel_addowner(server_data, token1, priv_channel_id, u_id2) 

    with pytest.raises(InputError) as error_raise:
        channel_addowner(server_data, token1, pub_channel_id, u_id1) 

    with pytest.raises(InputError) as error_raise:
        channel_addowner(server_data, token1, priv_channel_id, u_id1) 

def test_channel_addowner_user_not_channel_owner(auth_fixture):
    '''
    Test case when authorised user is not an owner of the channel or not an owner of slack
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user data
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    u_id2 = auth_fixture[2]['u_id']
    u_id3 = auth_fixture[3]['u_id']

    # create channels with 1 user (user 1 is owner)
    pub_channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    priv_channel_id = channels_create(server_data, token1, 'Priv_Channel', False)['channel_id']

    # user2 and user3 join channels
    channel_invite(server_data, token1, pub_channel_id, u_id2)
    channel_invite(server_data, token1, pub_channel_id, u_id3)
    channel_invite(server_data, token1, priv_channel_id, u_id2)
    channel_invite(server_data, token1, priv_channel_id, u_id3)

    # user2 (non slack or channel owner) tries to add user3 as an owner
    with pytest.raises(AccessError) as error_raise:
        channel_addowner(server_data, token2, pub_channel_id, u_id3)

    with pytest.raises(AccessError) as error_raise:
        channel_addowner(server_data, token2, priv_channel_id, u_id3)

def test_channel_addowner_user_slackr_owner(auth_fixture):
    '''
    Test case when authorised user is an owner of the slackr
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    tokenslackr = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    u_id2 = auth_fixture[2]['u_id']

    # create channels with 1 user (user 1 is owner)
    channel_id1 = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    channel_id2 = channels_create(server_data, token1, 'Another_Channel', True)['channel_id']
    
    # add user2 as member to channel1
    channel_invite(server_data, token1, channel_id1, u_id2)
    
    # slackrowner adds user2 as owner for channel1 (which user2 is a member of) and channel2 (which user2 is not a member of)
    channel_addowner(server_data, tokenslackr, channel_id1, u_id2) 
    channel_addowner(server_data, tokenslackr, channel_id2, u_id2) 

    # get details of channels
    user2_channel_det1 = channel_details(server_data, token2, channel_id1)['owner_members']
    user2_channel_det2 = channel_details(server_data, token2, channel_id2)['owner_members']

    # check that user2 is an owner for both channels
    assert any(True for i in user2_channel_det1 if i['u_id'] == u_id2)
    assert any(True for i in user2_channel_det2 if i['u_id'] == u_id2)

def test_channel_addowner_invalid_token(auth_fixture):
    '''
    Test case for invalid token
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details for user1 and user2
    token1 = auth_fixture[1]['token']
    u_id2 = auth_fixture[2]['u_id']
    
    # set an invalid token 
    invalid_token = '12345'

    # user1 creates channel 
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']

    # user1 trys to add user2 as owner with invalid token
    with pytest.raises(AccessError) as error_raise:
        channel_addowner(server_data, invalid_token, channel_id, u_id2)
