# pylint: disable=C0301, R0801
'''
Testing file for channel invite
When testing this function, we assume that all other functions work as expected

Assumptions:
- If an invitation is sent to a member of the channel, AccessError will be thrown
- When the owner of slackr is invited to the channel, they will automatically have ownership for the channel
- A member of the channel can send out invitation
- A user can be invited into a private channel
'''

import json
import urllib
import pytest
import constants as const
#from channel import channel_invite, channel_details

from helper_functions_t import does_member_exist_in_list

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

# Testing invalid token with valid channel_id and valid user_id, should return access error
def test_channel_invite_invalid_token(channels_http_fixture):
    """
    pytest: testing channel_invite with invalid token
    """

    channels_fixture = channels_http_fixture

    user_id = channels_fixture[0]["u_id"]
    channel_id = channels_fixture[2]["channels"][0]["channel_id"]
    token = "AMADEUPTOKEN"

    data = {
        "token": token,
        "channel_id": channel_id,
        "u_id": user_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    # this should throw AccessError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

# Testing invalid channels, input a fixture with no channels and try to invite with an invalid channel
def test_channel_invite_invalid_channel_id(auth_http_fixture):
    """
    pytest: testing channel_invite with invalid channel_id
    """

    auth_fixture = auth_http_fixture

    user3_token = auth_fixture[2]["token"]
    user1_id = auth_fixture[0]["u_id"]
    channel_id = 2415195

    data = {
        "token": user3_token,
        "channel_id": channel_id,
        "u_id": user1_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    # this should throw InputError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

# Using user3's token to invite an invalid user into channel owned by user3
def test_channel_invite_invalid_user(channels_http_fixture):
    """
    pytest: testing channel_invite with invalid user
    """

    channels_fixture = channels_http_fixture

    user3_token = channels_fixture[2]["token"]
    user3_channel = channels_fixture[2]["channels"][0]["channel_id"]

    user_id = 132131

    data = {
        "token": user3_token,
        "channel_id": user3_channel,
        "u_id": user_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    # this should throw InputError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

# Testing invitation of user 3 inviting user 2 into channel owned by user 4, should return an access error
def test_channel_invite_valid_channel_id_no_permission(channels_http_fixture):
    """
    pytest: testing channel_invite with no permission
    """

    channels_fixture = channels_http_fixture

    user3_token = channels_fixture[2]["token"]
    user2_id = channels_fixture[1]["u_id"]
    user4_channel = channels_fixture[3]["channels"][0]["channel_id"]

    data = {
        "token": user3_token,
        "channel_id": user4_channel,
        "u_id": user2_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    # this should throw InputError as the token is invalid
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

# Testing a double invite, using user3 to invite user2 into channel owned by user3 twice, it should succeed on first and fail with AccessError on second
def test_channel_invite_double_invite(channels_http_fixture):
    """
    pytest: testing channel_invite with double invites
    """

    channels_fixture = channels_http_fixture

    user3_token = channels_fixture[2]["token"]
    user2_id = channels_fixture[1]["u_id"]
    user3_channel = channels_fixture[2]["channels"][0]["channel_id"]

    data = {
        "token": user3_token,
        "channel_id": user3_channel,
        "u_id": user2_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # Second invite should fail
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

# Testing invitation into a private channel
# The private channel is fixture belong to user2 and user5
# ENG1001 and ADAD1010
# The member's id should show up in channel_details
def test_channel_invite_private_channel(channels_http_fixture):
    """
    pytest: testing channel_invite with private channels
    """

    channels_fixture = channels_http_fixture

    # Get user4 and user2's details
    user4 = channels_fixture[3]
    user2 = channels_fixture[1]

    # Get user 2's token and private channel ID
    user2_token = channels_fixture[1]["token"]
    user2_channel_info = channels_fixture[1]["channels"][0]

    data = {
        "token": user2_token,
        "channel_id": user2_channel_info["channel_id"],
        "u_id": user4["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)

    # After invitation, user4 should become a member of the channel 2
    channel_id = user2_channel_info["channel_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={user2_token}&channel_id={channel_id}")
    payload = json.load(response)

    channel_member_list = payload["all_members"]

    assert does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])

    # And user2 should still remain a member
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])

# Testing invitation into a public channel
# The public channel is fixture belong to user1, user3, user4
# The member's id should show up in channel_details
# User 1 will invite user 2 into the channel
def test_channel_invite_public_channel(channels_http_fixture):
    """
    pytest: testing channel_invite with public channel
    """

    channels_fixture = channels_http_fixture

    # Getting user 1 and user 2's info
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]

    # Getting user 1's channel info
    user1_channel_info = channels_fixture[0]["channels"][0]

    #invite user 2 into user 1's channel, as user 1
    data = {
        "token": user1["token"],
        "channel_id": user1_channel_info["channel_id"],
        "u_id": user2["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)

    # After nvitation, user 2 should become a member of the channel
    token = user1["token"]
    channel_id = user1_channel_info["channel_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)

    channel_member_list = payload["all_members"]

    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])

    # User 1 should also still be in the list
    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])

def test_channel_invite_multi_users(channels_http_fixture):
    """
    pytest: testing channel_invite with multi users
    """

    channels_fixture = channels_http_fixture

    # Getting all 5 user's info
    user1 = channels_fixture[0]
    user2 = channels_fixture[1]
    user3 = channels_fixture[2]
    user4 = channels_fixture[3]
    user5 = channels_fixture[4]

    # Retrieve the target channel: user3's channel
    user3_channel_info = user3["channels"][0]

    # Invite all users into the channel
    data = {
        "token": user3["token"],
        "channel_id": user3_channel_info["channel_id"],
        "u_id": user1["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)

    data = {
        "token": user3["token"],
        "channel_id": user3_channel_info["channel_id"],
        "u_id": user2["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)

    data = {
        "token": user3["token"],
        "channel_id": user3_channel_info["channel_id"],
        "u_id": user4["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)

    data = {
        "token": user3["token"],
        "channel_id": user3_channel_info["channel_id"],
        "u_id": user5["u_id"],
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)

    # After invitation, all 5 members should be a member of the channel
    # User1 should be the owner of the channel, as he is the super user
    token = user3["token"]
    channel_id = user3_channel_info["channel_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    payload = json.load(response)

    channel_member_list = payload["all_members"]
    channel_owner_list = payload["owner_members"]

    assert does_member_exist_in_list(channel_member_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_member_list, user2["u_id"], user2["name_first"], user2["name_last"])
    assert does_member_exist_in_list(channel_member_list, user3["u_id"], user3["name_first"], user3["name_last"])
    assert does_member_exist_in_list(channel_member_list, user4["u_id"], user4["name_first"], user4["name_last"])
    assert does_member_exist_in_list(channel_member_list, user5["u_id"], user5["name_first"], user5["name_last"])

    assert does_member_exist_in_list(channel_owner_list, user1["u_id"], user1["name_first"], user1["name_last"])
    assert does_member_exist_in_list(channel_owner_list, user3["u_id"], user3["name_first"], user3["name_last"])
