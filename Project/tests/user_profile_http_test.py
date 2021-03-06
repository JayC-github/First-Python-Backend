#pylint: disable=R0801
"""
Test module for users/profile in Slackr

Written by Robert Teoh for JRKS1531.
This file is independent of / separate from user_profile.py .

This module uses http requests through the server instead of
calling the functions in user.py directly.

Error conditions:
    Token is not valid            -> AccessError
    user id is not valid          -> InputError
"""
import json
import urllib
import flask
import pytest
import constants as const

SERVER_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

#Helper functions
def reset_state():
    """
    Resets the state of the server using /workspace/reset.
    """
    data = {}
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{SERVER_URL}/workspace/reset", \
        data=json_data)
    urllib.request.urlopen(req)

def register_user_1():
    """
    Registers a test user, and returns the user's token and user ID.
    """
    data = {
        "email" : 'jess@test.com',
        "password" : 'ABC1234',
        "name_first" : 'Jess',
        "name_last" : "Wu"
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/auth/register", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    response = (urllib.request.urlopen(req))
    returned_payload = json.load(response)

    return returned_payload

def register_user_2():
    """
    Registers a test user, and returns the user's token and user ID.
    """
    data = {
        "email" : 'tim@test.com',
        "password" : 'DEF1234',
        "name_first" : 'Tim',
        "name_last" : "Zhang"
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/auth/register", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    response = (urllib.request.urlopen(req))
    returned_payload = json.load(response)

    return returned_payload

#Test functions
def test_http_user_profile_normal():
    '''
    Normal test case.

    Test with valid token and valid u_id.
    Verify that the returned user details are correct.
    '''
    reset_state()

    user_1 = register_user_1()
    user_2 = register_user_2()

    #Query for user 1's details
    '''
    data = {
        "token" : user_1['token'],
        "u_id" : user_1['u_id']
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    token = user_1["token"]
    u_id = user_1["u_id"]
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user'] == {
        'u_id': user_1['u_id'],
        'email': 'jess@test.com',
        'name_first': 'Jess',
        'name_last': 'Wu',
        'handle_str': 'jesswu',
        'profile_img_url': ''
    }

    #Query for user 2's details
    '''
    data = {
        "token" : user_1['token'],
        "u_id" : user_2['u_id']
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    token = user_1["token"]
    u_id = user_2["u_id"]
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user'] == {
        'u_id': user_2['u_id'],
        'email': 'tim@test.com',
        'name_first': 'Tim',
        'name_last': 'Zhang',
        'handle_str': 'timzhang',
        'profile_img_url': ''
    }

def test_http_user_profile_no_token():
    '''
    Test with empty token. Query with valid u_id.
    AccessError will occur.
    '''

    reset_state()

    user_1 = register_user_1()
    register_user_2()

    #Query for user 1's details
    '''
    data = {
        "token" : '',
        "u_id" : user_1['u_id']
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    u_id = user_1['u_id']
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/user/profile?token=&u_id={u_id}")

def test_http_user_profile_invalid_token():
    '''
    Test with invalid token. Query with valid u_id.
    AccessError will occur.
    '''
    reset_state()

    user_1 = register_user_1()
    register_user_2()

    #Query for user 1's details
    '''
    data = {
        "token" : '0',
        "u_id" : user_1['u_id']
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    u_id = user_1['u_id']
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/user/profile?token=&u_id={u_id}")

def test_http_user_profile_no_id():
    '''
    Test with valid token. Query with empty u_id.
    InputError will occur.
    '''
    reset_state()

    user_1 = register_user_1()
    register_user_2()

    #Query for user 1's details
    '''
    data = {
        "token" : user_1['token'],
        "u_id" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    token = user_1["token"]
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id=")

def test_http_user_profile_no_id_no_token():
    '''
    Test with empty token. Query with empty u_id.
    AccessError will occur.
    '''
    reset_state()

    register_user_1()
    register_user_2()

    #Query for user 1's details
    '''
    data = {
        "token" : '',
        "u_id" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/user/profile?token=&u_id=")

def test_http_user_profile_invalid_id():
    '''
    Test with valid token. Query with empty u_id.
    InputError will occur.
    '''
    reset_state()

    user_1 = register_user_1()
    user_2 = register_user_2()

    #Set invalid test ID
    test_id = 1
    id_is_valid = True
    while id_is_valid:
        test_id += 1
        if not test_id == user_1['u_id'] or user_2['u_id']:
            id_is_valid = False

    #Query for user 1's details
    '''
    data = {
        "token" : user_1['token'],
        "u_id" : test_id
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    token = user_1['token']
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={test_id}")

def test_http_user_profile_invalid_id_invalid_token():
    '''
    Test with invalid token. Query with invalid u_id.
    AccessError will occur.
    '''
    reset_state()

    user_1 = register_user_1()
    user_2 = register_user_2()

    #Set invalid test ID
    test_id = 1
    id_is_valid = True
    while id_is_valid:
        test_id += 1
        if not test_id == user_1['u_id'] or user_2['u_id']:
            id_is_valid = False

    #Query for user 1's details
    '''
    data = {
        "token" : '0',
        "u_id" : test_id
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile", method="GET", \
        data=json_data, headers={'Content-Type' : 'application/json'})
    '''
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/user/profile?token=0&u_id={test_id}")
