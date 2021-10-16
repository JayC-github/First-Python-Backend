#pylint: disable=C0301,W0105,R0915
#pylint: disable=R0801
'''
Test file for function channels_listall
When testing this function, we assume that all other functions work as expected

Assumptions:
channels_listall will show all channels, including the private channels
'''

import pytest
from error import AccessError
from channels import channels_listall
from channel import channel_addowner, channel_removeowner
from helper_functions_t import does_channel_exist_in_list


# Testing invalid token with pre-filled fixture with 5 registered users, should still return AccessError
def test_invalid_token_with_users(auth_fixture):
    """
    Pytest: testing with invalid token
    """

    (server_data, auth_fixture) = auth_fixture
    token = "AMADEUPTOKEN2"

    # this should throw AccessError as the token is invalid
    with pytest.raises(AccessError):
        channels_listall(server_data, token)

def test_token_with_no_channels(auth_fixture):
    """
    Pytest: testing with invalid channels
    """

    (server_data, auth_fixture) = auth_fixture

    # Import the token infos
    user1 = auth_fixture[0]
    user2 = auth_fixture[1]
    user3 = auth_fixture[2]
    user4 = auth_fixture[3]
    user5 = auth_fixture[4]

    # Perform channels_listall on each of the user tokens
    # And output data into individual variables
    rt_val = channels_listall(server_data, user1["token"])
    channels_user1 = rt_val["channels"]
    rt_val = channels_listall(server_data, user2["token"])
    channels_user2 = rt_val["channels"]
    rt_val = channels_listall(server_data, user3["token"])
    channels_user3 = rt_val["channels"]
    rt_val = channels_listall(server_data, user4["token"])
    channels_user4 = rt_val["channels"]
    rt_val = channels_listall(server_data, user5["token"])
    channels_user5 = rt_val["channels"]

    # All of them should be empty
    assert len(channels_user1) == 0
    assert len(channels_user2) == 0
    assert len(channels_user3) == 0
    assert len(channels_user4) == 0
    assert len(channels_user5) == 0

'''
Because the function shows all channels, it should show every channel that has been created
'''
def test_token_with_channels(channels_fixture):
    """
    Pytest: testing with valid channels
    """

    (server_data, channels_fixture) = channels_fixture

    # Import the user info
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # Extract the channel info from users
    channels_list1 = user1["channels"]
    channels_list2 = user2["channels"]
    channels_list3 = user3["channels"]
    channels_list4 = user4["channels"]
    channels_list5 = user5["channels"]

    # Each of the listall should contain the same thing
    # user1
    rt_val = channels_listall(server_data, user1["token"])
    channels_user = rt_val["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    # user2
    rt_val = channels_listall(server_data, user2["token"])
    channels_user = rt_val["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    # user3
    rt_val = channels_listall(server_data, user3["token"])
    channels_user = rt_val["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    #user4
    rt_val = channels_listall(server_data, user4["token"])
    channels_user = rt_val["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

    #user5
    rt_val = channels_listall(server_data, user2["token"])
    channels_user = rt_val["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])

"""
Testing channels_listall should return the same after changes in membership/ownership 
"""
def test_token_with_channels_n_changes(channels_fixture):
    """
    Pytest: testing with channels and after changes
    """

    (server_data, channels_fixture) = channels_fixture

    # Import the user info
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # Extract the channel info from users
    channels_list1 = user1["channels"]
    channels_list2 = user2["channels"]
    channels_list3 = user3["channels"]
    channels_list4 = user4["channels"]
    channels_list5 = user5["channels"]

    # Making several changes to membership and ownership
    # Add user5 to COMP1531
    # Remove user1 from COMP1531
    # add user2 to COMP3221
    # remove user4 to COMP3221
    channel_addowner(server_data, user1["token"], channels_list1[0]["channel_id"], user5["u_id"])
    channel_addowner(server_data, user4["token"], channels_list4[0]["channel_id"], user2["u_id"])

    channel_removeowner(server_data, user1["token"], channels_list1[0]["channel_id"], user5["u_id"])
    channel_removeowner(server_data, user4["token"], channels_list4[0]["channel_id"], user4["u_id"])

    #The list of channels should remain the same
    rt_val = channels_listall(server_data, user1["token"])
    channels_user = rt_val["channels"]

    assert does_channel_exist_in_list(channels_user, channels_list1[0]["channel_id"], channels_list1[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list1[1]["channel_id"], channels_list1[1]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list2[0]["channel_id"], channels_list2[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list3[0]["channel_id"], channels_list3[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list4[0]["channel_id"], channels_list4[0]["name"])
    assert does_channel_exist_in_list(channels_user, channels_list5[0]["channel_id"], channels_list5[0]["name"])
