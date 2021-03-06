#pylint: disable=R0801
"""
auth_logout_http_test
"""
import urllib
import json
import constants as const
#import pytest
#import flask # needed for urllib.parse
#from server_data_class import Server_data
#from auth import auth_register, auth_login, auth_logout


#Access Error
#- Invalid token (logout before login)
#- Double logout

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"


def test_http_empty_token():
    """
    Pytest function to test empty token being entered into the function
    - The user should not logout successfully, a InputError should be thrown
    """
    # reset the workspace
    reset = json.dumps({}).encode('utf-8')
    req_re = urllib.request.Request(f"{BASE_URL}/workspace/reset", \
        data=reset, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req_re)

    # empty token
    data = json.dumps({
        "token": ""
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert not payload['is_success']

def test_http_double_logout():
    """
    Pytest function to test valid token being entered into the function
    - The user should logout successfully
    Then try to use the same token(invalid) to logout again
    - The user should not logout successfully, a InputError should be thrown
    """
    # reset the workspace
    reset = json.dumps({}).encode('utf-8')
    req_re = urllib.request.Request(f"{BASE_URL}/workspace/reset", \
        data=reset, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req_re)
    # registered user
    data = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req1))

    # token return by auth_register
    token = payload['token']

    # valid token by auth_register
    data_logout = json.dumps({
        "token": token
    }).encode('utf-8')

################################################################################
    data_login = json.dumps({
        "email": 'jay.chen@unsw.edu.au',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req2 = urllib.request.Request(f"{BASE_URL}/auth/login", data=data_login, \
        headers={'Content-Type': 'application/json'})

    payload = json.load(urllib.request.urlopen(req2))

    # token return by auth_login
    token2 = payload['token']

    # valid token by auth_login
    data_logout2 = json.dumps({
        "token": token2
    }).encode('utf-8')


################################################################################
    # first time use the token returned by auth_register, logout should success
    req3 = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data_logout, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req3))
    assert payload['is_success']

    # try to use the same token logout again, failed
    req4 = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data_logout, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req4))
    assert not payload['is_success']

    # use the token returned by auth_login, logout should success
    req5 = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data_logout2, \
    headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req5))
    assert payload['is_success']

    # try to use the same token logout again, failed
    req6 = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data_logout2, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req6))
    assert not payload['is_success']
