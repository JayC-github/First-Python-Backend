#pylint: disable=R0801
"""
auth_login_http_test
"""
import urllib
import json
import pytest
import constants as const
#import flask # needed for urllib.parse
#from server_data_class import Server_data
#from auth import auth_register, auth_login, auth_logout


#Input Error
#- Email entererd is not valid
#- Email entered does not belong to a user
#- password is not correct

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def reset_workspace():
    """
    reset the workspace
    """
    reset = json.dumps({}).encode('utf-8')
    req_re = urllib.request.Request(f"{BASE_URL}/workspace/reset", \
        data=reset, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req_re)

def test_invalid_email_login():
    """
    Pytest function to test invalid email being entered into the function
    - The user should not login successfully, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()
    # invalid email
    data = json.dumps({
        "email": 'jay.chen',
        "password": 'abcde123'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_not_user_login():
    """
    Pytest function to test Email entered does not belong to a user
    - The user should not login successfully, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    # email is valid but no belong to a user
    data = json.dumps({
        "email": 'jianjunjchen@gmail.com',
        "password": 'abcde123'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_incorrect_password_login():
    """
    Pytest function to test password is not correct
    - The user should not login successfully, a InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    # register user
    data = json.dumps({
        "email": 'MercyDuong@gmail.com',
        "password": '123456',
        "name_first": 'Mercy',
        "name_last": 'Duong'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})

    urllib.request.urlopen(req1)

    data_login = json.dumps({
        "email": 'MercyDuong@gmail.com',
        "password": 'abcde123'
    }).encode('utf-8')

    req2 = urllib.request.Request(f"{BASE_URL}/auth/login", data=data_login, \
        headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req2)

def test_http_login_normal():
    """
    Pytest function to test login success
    - The user should login successfully and return uid and token
    Input: JSON - {email, password}
    output: JSON - {u_id, token}
    """
    # reset the workspace
    reset_workspace()

    # registered user
    data = json.dumps({
        "email": 'jay.mercy@unsw.edu.au',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload1 = json.load(urllib.request.urlopen(req1))

    # uid and token return by auth_register
    u_id1 = payload1['u_id']
    token1 = payload1['token']

    data_login = json.dumps({
        "email": 'jay.mercy@unsw.edu.au',
        "password": '123456'
    }).encode('utf-8')

    req2 = urllib.request.Request(f"{BASE_URL}/auth/login", data=data_login, \
        headers={'Content-Type': 'application/json'})

    payload2 = json.load(urllib.request.urlopen(req2))
    u_id2 = payload2['u_id']
    token2 = payload2['token']

    # the return user id from auth_register and auth_login shoud be the same
    # and token shoud not
    assert u_id1 == u_id2
    assert token1 != token2
