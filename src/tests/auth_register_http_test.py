#pylint: disable=R0801
"""
auth_register_http_test
"""
import urllib
import json
import pytest
import constants as const
#import flask # needed for urllib.parse
#from error import InputError, AccessError # no module name error?
#from auth import auth_register, auth_login, auth_logout # no module name auth?


#Input Error
#- Email entererd is not valid
#- Email address is already being used by another user
#- password entered is less than 6 characters long
#- name first is not between 1-50 characters in length
#- name last is not between 1-50 characters in length


BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def reset_workspace():
    """
    reset the workspace
    """
    reset = json.dumps({}).encode('utf-8')
    req_re = urllib.request.Request(f"{BASE_URL}/workspace/reset", \
        data=reset, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req_re)

def test_http_invalid_email():
    """
    Pytest function to test invalid email being entered into the function
    - The user should not be created, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    # not invalid email
    data = json.dumps({
        "email": 'jay.chen',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_http_register_password():
    """
    Pytest function to test password entered is less than 6 characters long
    - The user should not be created, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_first_name_long():
    """
    Pytest function to test name first is not between 1-50 characters in length
    - The user should not be created, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": 'J'*51,
        "name_last": 'Chen'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_first_name_empty():
    """
    Pytest function to test name first is empty
    - The user should not be created, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": '',
        "name_last": 'Chen'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_last_name_long():
    """
    Pytest function to test name last is not between 1-50 characters in length
    - The user should not be created, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'C'*51
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_last_name_empty():
    """
    Pytest function to test name last is empty
    - The user should not be created, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": ''
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)



def test_http_register_double():
    """
    Pytest function to test register success
    - The user should be created and return uid and token
    Input: JSON - {email, password, name_first, name_last}
    Output: JSON - {u_id, token}
    """
   # reset the workspace
    reset_workspace()

    # register user, success
    data = json.dumps({
        "email": 'mercy.duong@unsw.edu.au',
        "password": 'abcd1234',
        "name_first": 'Mercy',
        "name_last": 'Duong'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})

    urllib.request.urlopen(req1)
    #u_id = payload1['u_id']
    #token = payload1['token']

    data2 = json.dumps({
        "email": 'mercy.duong@unsw.edu.au',
        "password": '1234abcd',
        "name_first": 'Mercy',
        "name_last": 'Duong'
    }).encode('utf-8')

    # try to register using the same email again, fail
    req2 = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data2, headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req2)



def test_http_register_normal():
    """
    Pytest function to test register success
    - The user should be created and return uid and token
    Input: JSON - {email, password, name_first, name_last}
    Output: JSON - {u_id, token}
    """
    # reset the workspace
    reset_workspace()

    # register user
    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", \
        data=data, headers={'Content-Type': 'application/json'})

    payload1 = json.load(urllib.request.urlopen(req1))
    u_id = payload1['u_id']
    token = payload1['token']

    # use user_profile to check if it registered successfully
    response = urllib.request.urlopen(f"{BASE_URL}/user/profile?token={token}&u_id={u_id}")
    payload2 = json.load(response)

    assert payload2['user']['u_id'] == u_id
    assert payload2['user']['email'] == 'jay.chen@unsw.edu.au'
    assert payload2['user']['name_first'] == 'Jay'
    assert payload2['user']['name_last'] == 'Chen'
