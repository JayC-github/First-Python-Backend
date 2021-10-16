#pylint: disable=R0801
"""
Test module for user/profile/setname in Slackr

Written by Robert Teoh for JRKS1531.
This file is independent of / separate from users_profile_setname_test.py .

This module uses http requests through the server instead of
calling the functions in user.py directly.

Error conditions:
    Token is not valid                    -> AccessError
    First name or last name is not valid  -> InputError
"""

import json
import urllib
import flask
import pytest
import constants as const

from error import AccessError

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


#Test functions
def test_http_user_profile_setname_normal():
    '''
    Normal test case.

    Test with valid token, valid firstname, valid lastname
    Verify that the details were updated correctly.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : 'first',
        "name_last" : 'last'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})
    response = (urllib.request.urlopen(req))
    returned_payload = json.load(response)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'first'
    assert returned_payload['user']['name_last'] == 'last'

def test_http_user_profile_setname_invalid_token():
    '''
    Test with invalid token, valid firstname, valid lastname.
    AccessError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '0',
        "name_first" : 'first',
        "name_last" : 'last'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_no_token():
    '''
    Test with invalid (empty) token, valid firstname, valid lastname
    AccessError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '',
        "name_first" : 'first',
        "name_last" : 'last'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_no_first_name():
    '''
    Test with valid token, no firstname, valid lastname
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : '',
        "name_last" : 'last'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_no_last_name():
    '''
    Test with valid token, valid firstname, no lastname
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : 'first',
        "name_last" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_no_name():
    '''
    Test with valid token, no firstname, no lastname
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : '',
        "name_last" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_no_token_no_name():
    '''
    Test with valid token, no firstname, no lastname
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '',
        "name_first" : '',
        "name_last" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_first_too_long():
    '''
    Test with valid token, invalid firstname (too long), valid lastname
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : 'x'*51,
        "name_last" : 'last'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_last_too_long():
    '''
    Test with valid token, valid firstname, invalid lastname (too long)
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : 'first',
        "name_last" : 'x'*51
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'

def test_http_user_profile_setname_first_and_last_too_long():
    '''
    Test with valid token, invalid firstname (too long), invalid lastname (too long)
    InputError should occur.
    Verify that the details were not updated.
    '''
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "name_first" : 'z'*51,
        "name_last" : 'x'*51
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setname", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['name_first'] == 'Jess'
    assert returned_payload['user']['name_last'] == 'Wu'
