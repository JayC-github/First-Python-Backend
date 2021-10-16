#pylint: disable=R0801
'''
Test file for function channel_removeowner
When testing this function, we assume that all other functions work as expected
'''
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
#pylint: disable=unused-variable
import pytest
from error import InputError, AccessError
from channels import channels_create, channels_listall
from channel import channel_removeowner, channel_invite, channel_details, channel_addowner

def test_channel_removeowner(auth_fixture):
    '''
    Test case for a simple channel removeowner
    - owner removing another owner in the same channel
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channels with user1 then add user2 as owner
    pub_channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    priv_channel_id = channels_create(server_data, token1, 'Priv_Channel', False)['channel_id']
    channel_addowner(server_data, token1, pub_channel_id, uid2)
    channel_addowner(server_data, token1, priv_channel_id, uid2) 
    
    # user1 removes user2 from owner permissions
    channel_removeowner(server_data, token1, pub_channel_id, uid2)
    channel_removeowner(server_data, token1, priv_channel_id, uid2)

    # check channel details to make sure user 2 is a non owner member
    user2_channel_det1 = channel_details(server_data, token2, pub_channel_id)['owner_members']
    user2_channel_det2 = channel_details(server_data, token2, priv_channel_id)['owner_members']
    
    # owner member list should not have any ids equal to the id of user2 
    assert not any(True for i in user2_channel_det1 if i['u_id'] == uid2)
    assert not any(True for i in user2_channel_det2 if i['u_id'] == uid2)

def test_channel_removeowner_invalid_channel_id(channels_fixture):
    '''
    Test case for invalid channel ID 
    '''
    (server_data, channels_fixture) = channels_fixture
    # get user details
    token_owner1 = channels_fixture[1]["token"]
    uid_owner2 = channels_fixture[2]["u_id"]

    # create channels with user1 then add user2 as owner
    channel_id = channels_create(server_data, token_owner1, 'New_Channel', True)['channel_id']
    channel_addowner(server_data, token_owner1, channel_id, uid_owner2)

    all_channels = channels_listall(server_data, token_owner1)

    # as defined in data types where all variables with suffix _id will be an integer
    channel_id_list = [x["channel_id"] for x in all_channels['channels']]
    invalid_channel_id = max(channel_id_list) + 1

    # check if removeowner works with a valid user but invalid channel id
    with pytest.raises(InputError) as error_raise:
        channel_removeowner(server_data, token_owner1, invalid_channel_id, uid_owner2)

def test_channel_removeowner_not_owner(auth_fixture):
    '''
    Test case for removing user when user is not an owner of the channel
    '''
    (server_data, auth_fixture) = auth_fixture
    # user1 and create a channel (user1 will be owner of channel)
    token1 = auth_fixture[1]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channel with 1 user (user 1 is owner)
    channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']

    # user1 adds user2 as non owner member
    channel_invite(server_data, token1, channel_id, uid2)

    # user1 removes user2 as owner (InputError should pop up)
    with pytest.raises(InputError) as error_raise:
        channel_removeowner(server_data, token1, channel_id, uid2) 

def test_channel_removeowner_user_not_channel_owner(auth_fixture):
    '''
    Test case when authorised user is not an owner of the channel and is not an owner of the slackr
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user data
    token1 = auth_fixture[1]['token']
    token3 = auth_fixture[3]['token']
    uid2 = auth_fixture[2]['u_id']
    uid3 = auth_fixture[3]['u_id']

    # create channels with 1 user (user 1 is owner)
    pub_channel_id = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    priv_channel_id = channels_create(server_data, token1, 'Priv_Channel', False)['channel_id']

    # user2 joins as owner
    channel_addowner(server_data, token1, pub_channel_id, uid2) 
    channel_addowner(server_data, token1, priv_channel_id, uid2) 

    # user3 join channels as member
    channel_invite(server_data, token1, pub_channel_id, uid3)
    channel_invite(server_data, token1, priv_channel_id, uid3)

    # user3 tries to remove user2 from ownership
    with pytest.raises(AccessError) as error_raise:
        channel_removeowner(server_data, token3, pub_channel_id, uid2)

    with pytest.raises(AccessError) as error_raise:
        channel_removeowner(server_data, token3, priv_channel_id, uid2) 

def test_channel_removeowner_user_slackr_owner(auth_fixture):
    '''
    Test case when authorised user is an owner of the slackr
    '''
    (server_data, auth_fixture) = auth_fixture
    # get user details
    tokenslackr = auth_fixture[0]['token']
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    u_id2 = auth_fixture[2]['u_id']

    # create channels with 1 user (user1 is owner)
    channel_id1 = channels_create(server_data, token1, 'New_Channel', True)['channel_id']
    channel_id2 = channels_create(server_data, token1, 'Another_Channel', True)['channel_id']
    
    # user1 adds user2 as member of channels
    channel_addowner(server_data, token1, channel_id1, u_id2) 
    channel_addowner(server_data, token1, channel_id2, u_id2) 

    # slackruser removes user2 from owner
    channel_removeowner(server_data, tokenslackr, channel_id1, u_id2) 
    channel_removeowner(server_data, tokenslackr, channel_id2, u_id2) 

    # get details of channels
    user2_channel_det1 = channel_details(server_data, token2, channel_id1)['owner_members']
    user2_channel_det2 = channel_details(server_data, token2, channel_id2)['owner_members']

    # check that user2 is not an owner for both channels
    assert not any(True for i in user2_channel_det1 if i['u_id'] == u_id2)
    assert not any(True for i in user2_channel_det2 if i['u_id'] == u_id2)

def test_channel_removeowner_invalid_token(auth_fixture):
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
    channel_addowner(server_data, token1, channel_id, uid2)     

    # user1 trys to remove user2 as owner with invalid token
    with pytest.raises(AccessError) as error_raise:
        channel_removeowner(server_data, invalid_token, channel_id, uid2)
