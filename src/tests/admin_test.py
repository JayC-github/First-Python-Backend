#pylint: disable=C0301, R0801
"""
Admin_test
a file to test the admin permission change function
"""

import pytest

import constants as const
from error import InputError, AccessError
from admin import admin_userpermission_change
from channels import channels_create
from channel import channel_join, channel_details

def test_admin_invalid_token(auth_fixture):
    """
    Pytest: testing invalid token
    """

    (server_data, auth_fixture) = auth_fixture
    token = "testtokenrandom"
    u_id = auth_fixture[0]["u_id"]

    with pytest.raises(AccessError):
        admin_userpermission_change(server_data, token, u_id, const.PERMISSION_GLOBAL_MEMBER)

def test_admin_invalid_u_id(auth_fixture):
    """
    Pytest: testing invalid u_id
    """

    (server_data, auth_fixture) = auth_fixture
    token = auth_fixture[0]["token"]
    u_id = 12414910

    with pytest.raises(InputError):
        admin_userpermission_change(server_data, token, u_id, const.PERMISSION_GLOBAL_MEMBER)

def test_admin_invalid_permmission_id(auth_fixture):
    """
    Pytest: testing invalid permission_id
    """

    (server_data, auth_fixture) = auth_fixture
    token = auth_fixture[0]["token"]
    u_id = auth_fixture[1]["u_id"]

    with pytest.raises(InputError):
        admin_userpermission_change(server_data, token, u_id, 3)

def test_admin_no_permission(auth_fixture):
    """
    Pytest: testing no permission
    """

    (server_data, auth_fixture) = auth_fixture
    token = auth_fixture[1]["token"]
    u_id = auth_fixture[0]["u_id"]

    with pytest.raises(AccessError):
        admin_userpermission_change(server_data, token, u_id, const.PERMISSION_GLOBAL_MEMBER)

def test_admin_valid_permission_change(auth_fixture):
    """
    Pytest: testing valid requests
    """
    (server_data, auth_fixture) = auth_fixture

    token = auth_fixture[0]["token"]
    token1 = auth_fixture[1]["token"]
    token2 = auth_fixture[2]["token"]
    token3 = auth_fixture[3]["token"]
    token4 = auth_fixture[4]["token"]

    u_id1 = auth_fixture[1]["u_id"]
    u_id2 = auth_fixture[2]["u_id"]
    u_id3 = auth_fixture[3]["u_id"]
    u_id4 = auth_fixture[4]["u_id"]

    # Change all of them to owner
    admin_userpermission_change(server_data, token, u_id1, const.PERMISSION_GLOBAL_OWNER)
    admin_userpermission_change(server_data, token, u_id2, const.PERMISSION_GLOBAL_OWNER)
    admin_userpermission_change(server_data, token, u_id3, const.PERMISSION_GLOBAL_OWNER)
    admin_userpermission_change(server_data, token, u_id4, const.PERMISSION_GLOBAL_OWNER)

    # user 0 now create a channel
    channel_info = channels_create(server_data, token, "TEST1", True)

    # All other users join the channel, they should automatically become owners
    channel_join(server_data, token1, channel_info["channel_id"])
    channel_join(server_data, token2, channel_info["channel_id"])
    channel_join(server_data, token3, channel_info["channel_id"])
    channel_join(server_data, token4, channel_info["channel_id"])

    # Get channel details and check
    rt_info = channel_details(server_data, token, channel_info["channel_id"])
    assert len(rt_info["owner_members"]) == 5
    assert len(rt_info["all_members"]) == 5

    # Test other users to change permission, it should not fail
    admin_userpermission_change(server_data, token2, u_id1, const.PERMISSION_GLOBAL_MEMBER)
    admin_userpermission_change(server_data, token2, u_id3, const.PERMISSION_GLOBAL_MEMBER)
    admin_userpermission_change(server_data, token2, u_id4, const.PERMISSION_GLOBAL_MEMBER)

    # Create a second channel to test
    channel_info = channels_create(server_data, token, "TEST1", True)
    channel_join(server_data, token1, channel_info["channel_id"])
    channel_join(server_data, token2, channel_info["channel_id"])
    channel_join(server_data, token3, channel_info["channel_id"])
    channel_join(server_data, token4, channel_info["channel_id"])

    # Get channel details and check
    rt_info = channel_details(server_data, token, channel_info["channel_id"])
    assert len(rt_info["owner_members"]) == 2
    assert len(rt_info["all_members"]) == 5
