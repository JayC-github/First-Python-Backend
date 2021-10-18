#pylint: disable=W0612
"""
A file to test remove_user function of the backend server
"""


import pytest
from remove_user import remove_user
from error import InputError, AccessError
from user import users_all
from channel import channel_details


def test_remove_user_invalid_token(channels_fixture):
    """
    A function to test remove user with invalid token
    It should raise AccessError
    """
    (server_data, channels_fixture) = channels_fixture
    token = "randomtoken"
    u_id = channels_fixture[1]["u_id"]

    with pytest.raises(AccessError):
        remove_user(server_data, token, u_id)





def test_remove_user_invalid_id(channels_fixture):
    """
    A function to test remove user with invalid target u_id
    It should raise InputError
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[0]["token"]
    u_id = 104014014

    with pytest.raises(InputError):
        remove_user(server_data, token, u_id)


def test_remove_user_no_permission(channels_fixture):
    """
    A function to test remove user with invalid permission
    It should raise AccessError
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[2]["u_id"]

    with pytest.raises(AccessError):
        remove_user(server_data, token, u_id)


def test_remove_user_remove_themselves(channels_fixture):
    """
    A function to test remove user with invalid target u_id
    It should raise AccessError
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[0]["token"]
    u_id = channels_fixture[0]["u_id"]

    with pytest.raises(AccessError):
        remove_user(server_data, token, u_id)





def test_remove_user_no_channels(auth_fixture):
    """
    A function to test removing user without any channels
    It should complete and the user should be gone from the database
    """
    (server_data, auth_fixture) = auth_fixture
    token = auth_fixture[0]["token"]
    token1 = auth_fixture[1]["token"]
    u_id1 = auth_fixture[1]["u_id"]

    assert len(users_all(server_data, token)["users"]) == 5

    # Removing user 1 out of the data
    remove_user(server_data, token, u_id1)
    assert len(users_all(server_data, token)["users"]) == 4

    # Using token 1 should be invalid, as the sessions are cleared
    with pytest.raises(AccessError):
        users_all(server_data, token1)



def test_remove_user_from_channels(channels_fixture):
    """
    A function to test removing users that were in a channel
    The user should be removed from the channel before deleted from the database
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[0]["token"]
    token1 = channels_fixture[2]["token"]
    u_id1 = channels_fixture[2]["u_id"]
    channel_id = channels_fixture[2]["channels"][0]["channel_id"]

    assert len(users_all(server_data, token)["users"]) == 5

    remove_user(server_data, token, u_id1)
    assert len(users_all(server_data, token)["users"]) == 4

    channel_info = channel_details(server_data, token, channel_id)
    assert len(channel_info["all_members"]) == 0
    assert len(channel_info["owner_members"]) == 0
