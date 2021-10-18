#pylint: disable=C0301, W0105
#pylint: disable=R0801
'''
Test file for function channels_list
When testing this function, we assume that all other functions work as expected
'''

import pytest
from error import AccessError
from channels import channels_list
from channel import channel_invite
from helper_functions_t import does_channel_exist_in_list

'''
Invalid token test, should return AccessError
'''

def test_invalid_tokens_with_users(auth_fixture):
    """
    Pytest: testing channels_list wiht invalid token
    """
    # make up values for input
    (server_data, auth_fixture) = auth_fixture
    token = "4444451AFA"

    # this should throw AccessError as the token is invalid
    with pytest.raises(AccessError):
        channels_list(server_data, token)

'''
Valid token tests with no channels, the users are pre-registered with fixture auth_fixture     
'''
def test_valid_token_no_channels(auth_fixture):
    """
    Pytest: testing channels_list with no channels
    """

    (server_data, auth_fixture) = auth_fixture

    # Split up the users
    user1 = auth_fixture[0]
    user2 = auth_fixture[1]
    user3 = auth_fixture[2]
    user4 = auth_fixture[3]
    user5 = auth_fixture[4]

    # For each user, use channels_list function, no channels should return
    rt_value = channels_list(server_data, user1["token"])
    channel_list1 = rt_value["channels"]

    rt_value = channels_list(server_data, user2["token"])
    channel_list2 = rt_value["channels"]

    rt_value = channels_list(server_data, user3["token"])
    channel_list3 = rt_value["channels"]

    rt_value = channels_list(server_data, user4["token"])
    channel_list4 = rt_value["channels"]

    rt_value = channels_list(server_data, user5["token"])
    channel_list5 = rt_value["channels"]

    # The length of the returned list should be 0
    assert len(channel_list1) == 0
    assert len(channel_list2) == 0
    assert len(channel_list3) == 0
    assert len(channel_list4) == 0
    assert len(channel_list5) == 0

'''
Using valid token and created channels from the channels_fixture to test that channel_list should only list channels that the user is a part of, instead of all channels
'''

def test_valid_token_owned_channels(channels_fixture):
    """
    Pytest: testing channels_list wiht owned channels
    """

    (server_data, channels_fixture) = channels_fixture

    #Split up the users:
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]


    #Extract the channel informations from the user
    channel_list1 = user1["channels"]
    channel_list2 = user2["channels"]

    # List channels for user 1
    rt_info = channels_list(server_data, user1["token"])
    channels_user1 = rt_info["channels"]

    # Check if it only contains the channels created by user1
    # user1 created two channels, COMP1531 and COMP2511, both public
    assert does_channel_exist_in_list(channels_user1, channel_list1[0]["channel_id"], channel_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user1, channel_list1[1]["channel_id"], channel_list1[1]["name"])

    # The channel name should match with the channel ID
    assert not does_channel_exist_in_list(channels_user1, channel_list1[0]["channel_id"], channel_list1[1]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list1[1]["channel_id"], channel_list1[0]["name"])

    # List channels for user 2
    rt_info = channels_list(server_data, user2["token"])
    channels_user2 = rt_info["channels"]

    # Check if it only contains the channels created by user2
    # user2 created one channel, ENG1001 it is private but since user2 is authorized, they should still see it

    assert does_channel_exist_in_list(channels_user2, channel_list2[0]["channel_id"], channel_list2[0]["name"])

    # The channel name should match with the channel ID
    assert not does_channel_exist_in_list(channels_user2, channel_list2[0]["channel_id"], "something random")
    assert not does_channel_exist_in_list(channels_user2, 99983, channel_list2[0]["name"])

    # Can add more users here

def test_valid_token_not_owned_channels(channels_fixture):
    """
    Pytest: testing channels_list with not owned channels
    """

    (server_data, channels_fixture) = channels_fixture

    #Split up the users:
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    #Extract the channel informations from the user
    channel_list2 = user2["channels"]
    channel_list3 = user3["channels"]
    channel_list4 = user4["channels"]
    channel_list5 = user5["channels"]

    # List channels for user 1
    rt_info = channels_list(server_data, user1["token"])
    channels_user1 = rt_info["channels"]

    # the channels from other users should not exist in this list
    # Because the user is not authorized
    assert not does_channel_exist_in_list(channels_user1, channel_list2[0]["channel_id"], channel_list2[0]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list3[0]["channel_id"], channel_list3[0]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list4[0]["channel_id"], channel_list4[0]["name"])
    assert not does_channel_exist_in_list(channels_user1, channel_list5[0]["channel_id"], channel_list5[0]["name"])

"""
The channel list include the channels a user is member of 
"""
def test_valid_token_member_channel(channels_fixture):
    """
    Pytest: testing channels_list with member channels
    """

    (server_data, channels_fixture) = channels_fixture

    #Split up the users:
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]

    #Extract the channel informations from the user
    channel_list1 = user1["channels"]
    channel_list2 = user2["channels"]

    #Now invite user2 into user1's channel
    channel_invite(server_data, user1["token"], channel_list1[0]["channel_id"], user2["u_id"])

    #Now user 2 should contain 2 channels, one owned, one as member
    rt_info = channels_list(server_data, user2["token"])
    channels_user2 = rt_info["channels"]

    assert does_channel_exist_in_list(channels_user2, channel_list1[0]["channel_id"], channel_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user2, channel_list2[0]["channel_id"], channel_list2[0]["name"])
