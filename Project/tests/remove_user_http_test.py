#pylint: disable=C0301, W0612
"""
A file to test remove_user function of the backend server
"""

import json
import urllib
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_remove_user_invalid_token(channels_http_fixture):
    """
    A function to test remove user with invalid token
    It should raise AccessError
    """

    token = "randomtoken"
    u_id = channels_http_fixture[1]["u_id"]

    data = {
        "token": token,
        "u_id": u_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/user/remove", method="DELETE", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)




def test_remove_user_invalid_id(channels_fixture):
    """
    A function to test remove user with invalid target u_id
    It should raise InputError
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[0]["token"]
    u_id = 104014014

    data = {
        "token": token,
        "u_id": u_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/user/remove", method="DELETE", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)



def test_remove_user_no_permission(channels_fixture):
    """
    A function to test remove user with invalid permission
    It should raise AccessError
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[1]["token"]
    u_id = channels_fixture[2]["u_id"]

    data = {
        "token": token,
        "u_id": u_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/user/remove", method="DELETE", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)




def test_remove_user_remove_themselves(channels_fixture):
    """
    A function to test remove user with invalid target u_id
    It should raise AccessError
    """
    (server_data, channels_fixture) = channels_fixture
    token = channels_fixture[0]["token"]
    u_id = channels_fixture[0]["u_id"]

    data = {
        "token": token,
        "u_id": u_id,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/user/remove", method="DELETE", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)





def test_remove_user_no_channels(auth_http_fixture):
    """
    A function to test removing user without any channels
    It should complete and the user should be gone from the database
    """

    token = auth_http_fixture[0]["token"]
    token1 = auth_http_fixture[1]["token"]
    u_id1 = auth_http_fixture[1]["u_id"]

    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert len(payload["users"]) == 5


    # Removing user 1 out of the data
    data = {
        "token": token,
        "u_id": u_id1,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/user/remove", method="DELETE", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert len(payload["users"]) == 4

    # Using token 1 should be invalid, as the sessions are cleared
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/users/all?token={token1}")






def test_remove_user_from_channels(channels_http_fixture):
    """
    A function to test removing users that were in a channel
    The user should be removed from the channel before deleted from the database
    """
    token = channels_http_fixture[0]["token"]
    token1 = channels_http_fixture[2]["token"]
    u_id1 = channels_http_fixture[2]["u_id"]
    channel_id = channels_http_fixture[2]["channels"][0]["channel_id"]

    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert len(payload["users"]) == 5

    data = {
        "token": token,
        "u_id": u_id1,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/user/remove", method="DELETE", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    response = urllib.request.urlopen(f"{BASE_URL}/users/all?token={token}")
    payload = json.load(response)
    assert len(payload["users"]) == 4

    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    channel_info = json.load(response)
    assert len(channel_info["all_members"]) == 0
    assert len(channel_info["owner_members"]) == 0
