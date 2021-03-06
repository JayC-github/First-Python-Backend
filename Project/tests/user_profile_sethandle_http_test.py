#pylint: disable=C0301
#pylint: disable=R0801
"""
Test module for user/profile/sethandle in Slackr

Written by Robert Teoh for JRKS1531.
This file is independent of / separate from user_profile_sethandle_test.

This module uses http requests through the server instead of
calling the functions in user.py directly.

Error conditions:
    Token is not valid            -> AccessError
    Handle is not valid           -> InputError
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
    req = urllib.request.Request(f"{SERVER_URL}/workspace/reset", data=json_data)
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
def test_http_user_profile_sethandle_normal():
    """
    Normal test case. All inputs are valid.
    Sets a user's handle, with valid, active token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "handle_str" : 'handle'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})
    response = (urllib.request.urlopen(req))
    returned_payload = json.load(response)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'handle'

def test_http_user_profile_sethandle_no_token():
    """
    Attempt to set a user's handle, with invalid (empty) token.
    AccessError should occur due to invalid token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : "",
        "handle_str" : 'testhandle'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

def test_http_user_profile_sethandle_invalid_token():
    """
    Attempt to set a user's handle, with invalid token.
    AccessError should occur due to invalid token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : "0",
        "handle_str" : 'testhandle'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

def test_http_user_profile_sethandle_no_handle():
    """
    Attempt to set a user's handle, with invalid handle (empty).
    InputError should occur due to invalid handle.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "handle_str" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

def test_http_user_profile_sethandle_no_token_no_handle():
    """
    Attempt to set a user's handle, with empty token and empty handle.
    AccessError should occur due to invalid token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '',
        "handle_str" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

def test_http_user_profile_sethandle_handle_too_short():
    """
    Attempt to set a user's handle, with invalid handle (too short).
    InputError should occur due to invalid handle.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "handle_str" : 'x'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

def test_http_user_profile_sethandle_handle_too_long():
    """
    Attempt to set a user's handle, with invalid handle (too short).
    InputError should occur due to invalid handle.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "handle_str" : 'thishandleistoolongandnotvalid'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

def test_http_user_profile_sethandle_handle_already_taken():
    """
    Attempt to set a user's handle, with an already-in-use handle.
    InputError should occur due to handle-already-in-use.
    """
    reset_state()

    user_1 = register_user_1()
    user_2 = register_user_2()

    #Attempt to set the email address of the user-2 to the email address of user-1
    data = {
        "token" : user_2['token'],
        "handle_str" : 'jesswu'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/sethandle", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    #Error should occur as email was already taken.
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that neither account was updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'jesswu'

    token = user_2['token']
    u_id = user_2['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['handle_str'] == 'timzhang'
