#pylint: disable=R0801
"""
Test module for user/profile/setemail in Slackr

Written by Robert Teoh for JRKS1531.
This file is independent of / separate from user_profile_setemail_test.

This module uses http requests through the server instead of
calling the functions in user.py directly.

Error conditions:
    Token is not valid            -> AccessError
    Email address is not valid    -> InputError
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

def test_http_user_profile_setemail_normal():
    """
    Normal test case. All inputs are valid.
    Sets a user's email, with valid, active token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "email" : 'newemail@test.com'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setemail", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})
    response = (urllib.request.urlopen(req))
    returned_payload = json.load(response)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'newemail@test.com'

def test_http_user_profile_setemail_invalid_email():
    """
    Attempt to set a user's email, with invalid email.
    InputError should occur due to invalid email.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : user_1['token'],
        "email" : 'newemailtest.com'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setemail", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'jess@test.com'

def test_http_user_profile_setemail_invalid_token():
    """
    Attempt to set a user's email, with invalid token.
    AccessError should occur due to invalid token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '0',
        "email" : 'newemail@test.com'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setemail", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'jess@test.com'

def test_http_user_profile_setemail_invalid_email_invalid_token():
    """
    Attempt to set a user's email, with invalid token and invalid email.
    AccessError should occur due to invalid token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '0',
        "email" : 'newemailtest.com'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setemail", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'jess@test.com'

def test_http_user_profile_setemail_empty_email_empty_token():
    """
    Attempt to set a user's email, with invalid (empty) token and invalid (empty) email.
    AccessError should occur due to invalid token.
    """
    reset_state()

    user_1 = register_user_1()

    data = {
        "token" : '',
        "email" : ''
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setemail", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that the account was not updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'jess@test.com'

def test_http_user_profile_setemail_email_already_taken():
    """
    Attempt to set a user's email, with an already-in-use email. All other inputs valid/acceptable.

    InputError should occur due to email-already-in-use.
    """
    reset_state()

    user_1 = register_user_1()
    user_2 = register_user_2()

    #Attempt to set the email address of the user-2 to the email address of user-1
    data = {
        "token" : user_2['token'],
        "email" : 'jess@test.com'
    }
    json_data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(f"{SERVER_URL}/user/profile/setemail", \
        method="PUT", data=json_data, headers={'Content-Type' : 'application/json'})

    #Error should occur as email was already taken.
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Verify that neither account was updated.
    token = user_1['token']
    u_id = user_1['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'jess@test.com'

    token = user_2['token']
    u_id = user_2['u_id']
    response = urllib.request.urlopen(f"{SERVER_URL}/user/profile?token={token}&u_id={u_id}")
    returned_payload = json.load(response)

    assert returned_payload['user']['email'] == 'tim@test.com'
