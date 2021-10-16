#pylint: disable=C0301, W0105
#pylint: disable=R0801
'''
Test file for function channels_create
When testing this function, we assume that all other functions work as expected

Assumption:
- A channel could have duplicated name, but the id should be unique
'''

import pytest
from error import InputError, AccessError
from channels import channels_create, channels_list, channels_listall
from channel import channel_details
from helper_functions_t import does_channel_exist_in_list, does_member_exist_in_list



'''
Used auth_fixture to initialize the program with 5 registered users
Invalid token:
- The channel should not be created, an AccessError should be thrown
'''
def test_invalid_tokens_public_with_users(auth_fixture):
    """
    Pytest: testing channels_create with invalid token
    """
    (server_data, auth_fixture) = auth_fixture
    # Testing creation of public channel
    # make up values for input
    token = "jealgjlejaiorja"
    name = "testroom"
    is_public = True

    with pytest.raises(AccessError):
        channels_create(server_data, token, name, is_public)

def test_invalid_tokens_private_with_users(auth_fixture):
    """
    Pytest: testing channels_create with invalid token
    """
    (server_data, auth_fixture) = auth_fixture
    # Testing creation of private channel
    # make up values for input
    token = "291410481hjahfj1"
    name = "testroom"
    is_public = False

    with pytest.raises(AccessError):
        channels_create(server_data, token, name, is_public)

'''
Using registered user initialized from auth_fixture to create a channel, but have invalid name inputs
'''
def test_invalid_name_input(auth_fixture):
    """
    Pytest: testing channels_create with invalid name
    """

    (server_data, auth_fixture) = auth_fixture

    #obtain the token first person in the initialization - richard
    token1 = auth_fixture[0]["token"]
    name = 'a' * 21

    with pytest.raises(InputError):
        channels_create(server_data, token1, name, True)
        channels_create(server_data, token1, name, False)

    #testing the same with another person
    token2 = auth_fixture[3]["token"]
    with pytest.raises(InputError):
        channels_create(server_data, token2, name, True)
        channels_create(server_data, token2, name, False)

'''
Using registered users to successfully create a channel, the channel should show up in the channels_list and channels_listall and operations regarding to the channel should succeed

The channel should be created with the correct information and can be found in the list
'''
def test_valid_channel_creation(auth_fixture):
    """
    Pytest: testing channels_create with valid channel creation
    """

    (server_data, auth_fixture) = auth_fixture
    # Split up the users
    user1 = auth_fixture[0]

    # register the first public channel for user1
    # Name: "COMP1000"
    # Channel ID: unknown, return from function

    channel_name = "COMP1000"
    return_val = channels_create(server_data, user1["token"], channel_name, True)
    channel_id = return_val['channel_id']
    # check if the return contains the correct type
    assert isinstance(channel_id, int)

    # The channel is successfully created, it should show up in other functions
    return_val = channels_list(server_data, user1["token"])
    # The only channel that should returned is the channel that were created
    channel_list = return_val["channels"]
    assert channel_list[0]["channel_id"] == channel_id
    assert channel_list[0]["name"] == "COMP1000"

    # Same thing should happen to channels_listall
    return_val = channels_listall(server_data, user1["token"])
    channel_list = return_val["channels"]
    assert channel_list[0]["channel_id"] == channel_id
    assert channel_list[0]["name"] == "COMP1000"

    # register the second channel, first private channel for user1, it should not overwrite the previous channel
    # Name: "ENG1001"
    # Channel ID: unknown, return from function
    channel_name2 = "ENG1001"
    return_val = channels_create(server_data, user1["token"], channel_name2, False)
    channel_id2 = return_val['channel_id']
    assert isinstance(channel_id2, int)

    # Now the user should have 2 channels in the list
    return_val = channels_list(server_data, user1["token"])
    channel_list2 = return_val["channels"]

    # The public channel should still exist
    assert does_channel_exist_in_list(channel_list2, channel_id, channel_name)
    assert does_channel_exist_in_list(channel_list2, channel_id2, channel_name2)

    # The channel ID and channel name should match
    assert not does_channel_exist_in_list(channel_list2, channel_id2, channel_name)
    assert not does_channel_exist_in_list(channel_list2, channel_id, channel_name2)

    # User1 should be the owner of the channel created
    return_val = channel_details(server_data, user1["token"], channel_id)
    channel_owner_list = return_val["owner_members"]
    channel_name3 = return_val["name"]
    assert channel_name3 == channel_name

    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])

'''
if __name__ == "__main__":

    channel_list =[{ 
        "channel_id" : 0, "name": "COMP1001"
    }, { 
        "channel_id" : 1, "name": "ENG1001"
    }] 

    print (does_channel_exist_in_list(channel_list, 0, "COMP1001"))
    print (does_channel_exist_in_list(channel_list, 1, "COMP1001"))
    print (does_channel_exist_in_list(channel_list, 1, "ENG1001"))

    name = 'a' * 21
    print (name)

'''
