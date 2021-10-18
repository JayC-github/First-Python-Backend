#pylint: disable=R0801
"""
Test module for users/all in Slackr

Written by Robert Teoh for JRKS1531.
This file is independent of / separate from users_all_test.py .

This module uses http requests through the server instead of
calling the functions in user.py directly.

Error conditions:
    Token is not valid            -> AccessError
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
def test_http_users_all_normal():
    '''
    Normal test case.

    Test with valid token.
    Verify that the returned user details are correct.
    '''

    reset_state()

    user_1 = register_user_1()
    user_2 = register_user_2()

    #Query for user 2's details
    token = user_1['token']
    response = urllib.request.urlopen(f"{SERVER_URL}/users/all?token={token}")
    returned_payload = json.load(response)


    assert returned_payload == {
        'users': [
            {
                'u_id': user_1['u_id'],
                'email': 'jess@test.com',
                'name_first': 'Jess',
                'name_last': 'Wu',
                'handle_str': 'jesswu',
                'profile_img_url': ''
            },

            {
                'u_id': user_2['u_id'],
                'email': 'tim@test.com',
                'name_first': 'Tim',
                'name_last': 'Zhang',
                'handle_str': 'timzhang',
                'profile_img_url': ''
            },
        ],
    }

def test_http_users_all_no_token():
    '''
    Test with no token.
    AccessError will occur.
    '''
    reset_state()

    register_user_1()
    register_user_2()

    #Query for user 2's details
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/users/all?token=")

def test_http_users_all_invalid_token():
    '''
    Test with invalid token.
    AccessError will occur.
    '''

    reset_state()

    register_user_1()
    register_user_2()

    #Query for user 2's details
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{SERVER_URL}/users/all?token=0")
