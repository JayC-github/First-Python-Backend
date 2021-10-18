#pylint: disable=C0301, W0621, W0105
#pylint: disable=R0801
"""
Conftest.py
a file for all available fixtures for testing
"""
import urllib
import json
import pytest
import auth
import channels
import constants as const

from server_data_class import Server_data


def data_set_one():
    """
    Dataset 1 - contains 5 users
    """
    user_list1 = [{
        "email" : "richard@gmail.com",
        "password" : "12345333",
        "name_first" : "Richard",
        "name_last" :  "Park",
    }, {
        "email" : "kevin@gmail.com",
        "password" : "099401010",
        "name_first" : "Kevin",
        "name_last" :  "Seu",
    }, {
        "email" : "steven@gmail.com",
        "password" : "312214141",
        "name_first" : "Steven",
        "name_last" :  "Yang",
    }, {
        "email" : "jay@gmail.com",
        "password" : "10003DDfe",
        "name_first" : "Jay",
        "name_last" :  "Chen",
    }, {
        "email" : "robert@gmail.com",
        "password" : "jfkw22131",
        "name_first" : "Robert",
        "name_last" :  "Teoh",
    }]

    return user_list1

def data_set_channels():
    """
    Dataset 1 - contains 6 channels
    """
    channel_list = [{
        "name" : "COMP1531",
        "is_public" : True,
    }, {
        "name" : "ENG1001",
        "is_public" : False,
    }, {
        "name" : "COMP3331",
        "is_public" : True,
    }, {
        "name" : "COMP3211",
        "is_public" : True,
    }, {
        "name" : "ADAD1010",
        "is_public" : False,
    }, {
        "name" : "COMP2511",
        "is_public" : True,
    }]

    return channel_list

# Register users for backend testing
def register_users(server_data, user_list_in):
    """
    Function to register user in the backend
    """
    user_list = user_list_in
    for user in user_list:
        #print (user["email"])
        user_token = auth.auth_register(server_data, user["email"], user["password"], user["name_first"], user["name_last"])
        user["u_id"] = user_token["u_id"]
        user["token"] = user_token["token"]

    return user_list

# Register users for http testing

# The user list is supposed to already contain the tokens
def register_channels(server_data, user_list_in, channel_list_in):
    """
    Function to register channels in the backend
    """
    user_list = user_list_in
    channel_list = channel_list_in
    pos = 0

    for user in user_list:
        channel_info = channel_list[pos]
        channel_id = channels.channels_create(server_data, user["token"], channel_info["name"], channel_info["is_public"])

        # add channel ID into the channel infos
        channel_info["channel_id"] = channel_id["channel_id"]

        # import the infos into user
        # Because no channel exists yet, we are hard coding the channel initialization into user
        user["channels"] = []
        user["channels"].append(channel_info)

        pos += 1

    # add one extra channel to the first user
    user = user_list_in[0]
    channel_info = channel_list[pos]
    channel_id = channels.channels_create(server_data, user["token"], channel_info["name"], channel_info["is_public"])
    channel_info["channel_id"] = channel_id["channel_id"]

    user_list[0]["channels"].append(channel_info)

    return user_list

'''
Python fixture for auth tests
Creates a list of 5 registered users infos stored in an dictionary using data_set_one() above.
Each of the user's email, password, name_first, name_last were pased into the auth_register function to obtain the valid u_id and token. Stored in key "u_id" and "token".
After calling the fixture, the program will contain 5 registered user with each of their active tokens and u_ids for testing

structure:
    auth_fixture (array of dics)
        for each user
        - email
        - password
        - name_first
        - name_last
        - u_id
        - token

Usage:
    def test_*****(auth_fixture):
        richard_token = auth_fixture[0]["token"]

'''


@pytest.fixture
def auth_fixture():
    """
    auth_fixture can also be used to initialize the tests for user functions, as it only requires users
    """
    server_data = Server_data()
    server_data.server_data_reset()

    user_list = register_users(server_data, data_set_one())
    return (server_data, user_list)

'''
Python fixture for channels tests
Creates a list of 5 registered users infos stored in an dictionary using data_set_one() above.

Each of the user's email, password, name_first, name_last were pased into the auth_register function to obtain the valid u_id and token. Stored in key "u_id" and "token".

The channels_create function is then called so that each user then have 1 channel, either private or public and the first person (richard) has 2 channels

After calling the fixture, the program will contain 5 registered user with each of their active tokens and u_ids for testing

structure:
    channels_fixture (array of dics)
        for each user
        - email
        - password
        - name_first
        - name_last
        - u_id
        - token
        - channels (array of dics)
            for each channel:
            - name (channel)
            - is_public
            - channel_id

Usage:
    def test_*****(channels_fixture):
        richard_token = auth_fixture[0]["token"]

'''

@pytest.fixture
def channels_fixture():
    """
    Python fixture for channels tests
    Creates a list of 5 registered users infos stored in an dictionary using data_set_one() above.
    """
    server_data = Server_data()
    server_data.server_data_reset()

    user_list = register_channels(server_data, register_users(server_data, data_set_one()), data_set_channels())

    assert server_data.num_channels() == 6

    return (server_data, user_list)

"""
HTTP fixtures 
"""

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def reset_server_http():
    """
    Function to reset server via http
    """
    data = {}
    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(post_req)

def register_users_http(user_list):
    """
    function to register users via http requests
    """
    for user in user_list:

        # Create data to send to the server
        data = {
            "email": user["email"],
            "password": user["password"],
            "name_first": user["name_first"],
            "name_last": user["name_last"],
        }

        json_data = json.dumps(data).encode('utf-8')
        post_req = urllib.request.Request(f"{BASE_URL}/auth/register", method="POST", data=json_data, headers={"Content-Type": "application/json"})
        response = urllib.request.urlopen(post_req)
        payload = json.load(response)

        user["u_id"] = payload["u_id"]
        user["token"] = payload["token"]

    return user_list

def register_channels_http(user_list, channel_list):
    """
    Function to register channels via http
    """

    pos = 0

    for user in user_list:
        channel_info = channel_list[pos]

        # Create data to send to the server
        data = {
            "token": user["token"],
            "name": channel_info["name"],
            "is_public": channel_info["is_public"],
        }

        json_data = json.dumps(data).encode('utf-8')
        post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
        response = urllib.request.urlopen(post_req)
        payload = json.load(response)

        #channel_id = channels.channels_create(server_data, user["token"], channel_info["name"], channel_info["is_public"])

        # add channel ID into the channel infos
        channel_info["channel_id"] = payload["channel_id"]

        # import the infos into user
        # Because no channel exists yet, we are hard coding the channel initialization into user
        user["channels"] = []
        user["channels"].append(channel_info)

        pos += 1

    # add one extra channel to the first user
    user = user_list[0]
    channel_info = channel_list[pos]

    # Create data to send to the server
    data = {
        "token": user["token"],
        "name": channel_info["name"],
        "is_public": channel_info["is_public"],
    }

    json_data = json.dumps(data).encode('utf-8')
    post_req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(post_req)
    payload = json.load(response)

    channel_info["channel_id"] = payload["channel_id"]

    user_list[0]["channels"].append(channel_info)

    return user_list

@pytest.fixture
def auth_http_fixture():
    """
    fixture for users via http methods
    """
    reset_server_http()
    user_list = register_users_http(data_set_one())
    return user_list

@pytest.fixture
def channels_http_fixture():
    """
    fixture for channels via http methods
    """
    reset_server_http()
    user_list = register_users_http(data_set_one())
    user_list = register_channels_http(user_list, data_set_channels())
    return user_list

'''
if __name__ == "__main__":

    dataTest = register_channels(register_users(data_set_one()), data_set_channels())
    for data in dataTest:
        print (data)

    dataTest = data_set_channels()
    for data in dataTest:
        if not data["is_public"]:
            print (data) 

'''
