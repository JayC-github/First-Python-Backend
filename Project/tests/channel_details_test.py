# pylint: disable=C0301, W0105, R0801
'''
Testing file for channel_details
When testing this function, we assume that all other functions work as expected

Assumption:
An owner will show up in both owner_members and all_member list
'''

import pytest
from error import InputError, AccessError
from channel import channel_invite, channel_details, channel_addowner, channel_join
from helper_functions_t import does_member_exist_in_list

# Invalid token is passed into the function, should return AccessError as expected
def test_channel_details_invalid_token(channels_fixture):
    """
    Function to test channel_details with invalid token
    """

    (server_data, channels_fixture) = channels_fixture

    channel_id = channels_fixture[2]["channels"][0]["channel_id"]
    token = "AMADEUPTOKEN"

    # this should throw AccessError as the token is invalid
    with pytest.raises(AccessError):
        channel_details(server_data, token, channel_id)

# Invalid Channel ID is passed into the function, should return InputError as expected
def test_channel_details_invalid_channel_id(channels_fixture):
    """
    Function to test channel_details with invalid channel_id
    """

    (server_data, channels_fixture) = channels_fixture

    token = channels_fixture[0]["token"]
    channel_id = 21414141511321

    # this should throw InputError as the channel is invalid/not exist
    with pytest.raises(InputError):
        channel_details(server_data, token, channel_id)

# Channel that the user has no permission of is passed into the function
def test_channel_details_no_permission(channels_fixture):
    """
    Function to test channel_details with no permissions
    """

    (server_data, channels_fixture) = channels_fixture

    token = channels_fixture[1]["token"]
    channel_id = channels_fixture[3]["channels"][0]["channel_id"]

    with pytest.raises(AccessError):
        channel_details(server_data, token, channel_id)

# Testing a channel with only one owner, should return the owner at both owner and member
def test_channel_with_only_owner(channels_fixture):
    """
    Function to test channel_details with only owners
    """

    (server_data, channels_fixture) = channels_fixture

    # unpack the fixtures into 5 separate users
    user = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # using user1 for channel details
    token = user["token"]
    channel_info = channels_fixture[0]["channels"][0]
    channel_id = channel_info["channel_id"]

    # obtain the channel detail from the functions
    rt_value = channel_details(server_data, token, channel_id)
    channel_name = rt_value["name"]
    channel_owner_list = rt_value["owner_members"]
    channel_member_list = rt_value["all_members"]

    # user1 should be both in owner's list and the member's list
    assert channel_name == channel_info["name"]
    assert does_member_exist_in_list(channel_owner_list, user["u_id"], user["name_first"], user["name_last"])
    assert does_member_exist_in_list(channel_member_list, user["u_id"], user["name_first"], user["name_last"])

    # No other users should show up
    assert not does_member_exist_in_list(channel_owner_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user5["u_id"], user5["name_first"], user5["name_last"])

    assert not does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])

def test_channel_with_extra_members(channels_fixture):
    """
    Function to test channel_details with extra members
    """

    (server_data, channels_fixture) = channels_fixture

    #unpack all 5 users
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # Select channel from user3 as the test channel
    channel = user3["channels"][0]

    # Invite all users into the channel
    channel_invite(server_data, user3["token"], channel["channel_id"], user1["u_id"])
    channel_invite(server_data, user3["token"], channel["channel_id"], user2["u_id"])
    channel_invite(server_data, user3["token"], channel["channel_id"], user4["u_id"])
    channel_invite(server_data, user3["token"], channel["channel_id"], user5["u_id"])

    # Now user1-5 should show up in all members, and user 1 as the owner of slackr, is now the owner of the channel

    rt_info = channel_details(server_data, user3["token"], channel["channel_id"])
    channel_name = rt_info["name"]
    channel_member_list = rt_info["all_members"]
    channel_owner_list = rt_info["owner_members"]

    # Check channel name
    assert channel_name == channel["name"]

    # Check member list
    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # Check owner list
    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])

    # Other members should not show up in the owner's list
    assert not does_member_exist_in_list(channel_owner_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user5["u_id"], user5["name_first"], user5["name_last"])

# Testing a channel that contains only owners
def test_channel_with_only_owners(channels_fixture):
    """
    Function to test channel_details with only owners
    """

    (server_data, channels_fixture) = channels_fixture

    #unpack all 5 users
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # Select channel from user2 as the test channel
    channel = user2["channels"][0]

    # Add all users to the ownership of the channel
    channel_addowner(server_data, user2["token"], channel["channel_id"], user1["u_id"])
    channel_addowner(server_data, user2["token"], channel["channel_id"], user3["u_id"])
    channel_addowner(server_data, user2["token"], channel["channel_id"], user4["u_id"])
    channel_addowner(server_data, user2["token"], channel["channel_id"], user5["u_id"])

    # Now all members should exist in both owner and member
    rt_info = channel_details(server_data, user2["token"], channel["channel_id"])
    channel_member_list = rt_info["all_members"]
    channel_owner_list = rt_info["owner_members"]

    # Checking the member list, all users should be in members
    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # Checking the owner list, all users should be in owners
    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user5["u_id"], user5["name_first"], user5["name_last"])

'''
The intention of this function is to test if a member can call details after it was invited/joined/added owner to the channel
'''
def test_channel_details_nested_call(channels_fixture):
    """
    Function to test channel_details with nested call
    """

    (server_data, channels_fixture) = channels_fixture

    # unpack all 5 users
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # select channel from user1 as the test channel
    channel = user1["channels"][0]

    # user2 will join the channel as member:
    channel_join(server_data, user2["token"], channel["channel_id"])

    # check that user 2 is now a member, not an owner and user 3-5 is not a member with user2's token
    rt_info = channel_details(server_data, user2["token"], channel["channel_id"])
    channel_member_list = rt_info["all_members"]
    channel_owner_list = rt_info["owner_members"]

    # Checking Owner's list, only 1 owner - user1
    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # Checking Member List , 2 members - user1 and user2
    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # Now user3 will join as an owner
    channel_addowner(server_data, user1["token"], channel["channel_id"], user3["u_id"])

    # Check that user 3 is now a owner, 4-5 is not a member with user3's token
    rt_info = channel_details(server_data, user3["token"], channel["channel_id"])
    channel_member_list = rt_info["all_members"]
    channel_owner_list = rt_info["owner_members"]

    # Checking Owner list, should contain user1 and user3
    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # checking Member List, should contain user 1-3
    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # Now user3 will invite user4 in
    channel_invite(server_data, user3["token"], channel["channel_id"], user4["u_id"])

    # Check that user 4 is now a member, 5 is not a member with user3's token
    rt_info = channel_details(server_data, user4["token"], channel["channel_id"])
    channel_member_list = rt_info["all_members"]
    channel_owner_list = rt_info["owner_members"]

    # checking Owner list, should still have only user 1 and 3
    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_owner_list, user5["u_id"], user5["name_first"], user5["name_last"])

    # checking Member List, should have user1-4
    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert not does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])
