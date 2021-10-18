#pylint: disable=C0301, R0914, R0915, R0801, W0105
"""
Admin_test
a file to test the admin permission change function
"""

import json
import urllib
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def test_admin_invalid_token(auth_http_fixture):
    """
    Pytest: testing invalid token
    """

    auth_fixture = auth_http_fixture
    token = "testtokenrandom"
    u_id = auth_fixture[0]["u_id"]

    # create data
    data = {
        "token": token,
        "u_id": u_id,
        "permission_id": const.PERMISSION_GLOBAL_MEMBER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_admin_invalid_u_id(auth_http_fixture):
    """
    Pytest: testing invalid u_id
    """

    auth_fixture = auth_http_fixture
    token = auth_fixture[0]["token"]
    u_id = 12414910

    # create data
    data = {
        "token": token,
        "u_id": u_id,
        "permission_id": const.PERMISSION_GLOBAL_MEMBER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_admin_invalid_permmission_id(auth_http_fixture):
    """
    Pytest: testing invalid permission_id
    """

    auth_fixture = auth_http_fixture
    token = auth_fixture[0]["token"]
    u_id = auth_fixture[1]["u_id"]

    # create data
    data = {
        "token": token,
        "u_id": u_id,
        "permission_id": 3
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_admin_no_permission(auth_http_fixture):
    """
    Pytest: testing no permission
    """

    auth_fixture = auth_http_fixture
    token = auth_fixture[1]["token"]
    u_id = auth_fixture[0]["u_id"]

    # create data
    data = {
        "token": token,
        "u_id": u_id,
        "permission_id": const.PERMISSION_GLOBAL_MEMBER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_admin_valid_permission_change(auth_http_fixture):
    """
    Pytest: testing valid requests
    """
    auth_fixture = auth_http_fixture

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
    # create data
    data = {
        "token": token,
        "u_id": u_id1,
        "permission_id": const.PERMISSION_GLOBAL_OWNER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    data = {
        "token": token,
        "u_id": u_id2,
        "permission_id": const.PERMISSION_GLOBAL_OWNER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    data = {
        "token": token,
        "u_id": u_id3,
        "permission_id": const.PERMISSION_GLOBAL_OWNER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    data = {
        "token": token,
        "u_id": u_id4,
        "permission_id": const.PERMISSION_GLOBAL_OWNER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # user 0 now create a channel
    data = {
        "token": token,
        "name": "TEST1",
        "is_public": True
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    channel_info = json.load(response)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token1,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token2,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token3,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token4,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # Get channel details and check
    '''
    data = {
        "token": token,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/details", method="GET", data=json_data, headers={"Content-Type": "application/json"})
    '''
    channel_id = channel_info["channel_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    rt_info = json.load(response)

    assert len(rt_info["owner_members"]) == 5
    assert len(rt_info["all_members"]) == 5

    # Test other users to change permission, it should not fail
    data = {
        "token": token2,
        "u_id": u_id1,
        "permission_id": const.PERMISSION_GLOBAL_MEMBER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    data = {
        "token": token2,
        "u_id": u_id3,
        "permission_id": const.PERMISSION_GLOBAL_MEMBER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    data = {
        "token": token2,
        "u_id": u_id4,
        "permission_id": const.PERMISSION_GLOBAL_MEMBER
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # Create a second channel to test
    data = {
        "token": token,
        "name": "TEST1",
        "is_public": True
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    channel_info = json.load(response)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token1,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token2,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token3,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    # All other users join the channel, they should automatically become owners
    data = {
        "token": token4,
        "channel_id": channel_info["channel_id"]
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


    # Get channel details and check
    channel_id = channel_info["channel_id"]
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?token={token}&channel_id={channel_id}")
    rt_info = json.load(response)

    assert len(rt_info["owner_members"]) == 2
    assert len(rt_info["all_members"]) == 5
