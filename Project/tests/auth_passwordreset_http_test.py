"""
auth_passwordreset_request
auth_passwordreset_reset
"""
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

def reset_workspace():
    """
    reset the workspace
    """
    reset = json.dumps({}).encode('utf-8')
    req_re = urllib.request.Request(f"{BASE_URL}/workspace/reset", \
        data=reset, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req_re)

def test_invalid_email_request():
    """
    Pytest function to test invalid email being entered into the function
    - The user should not get reset_code successfully, InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    # invalid email
    data = json.dumps({
        "email": 'jay.chen'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/passwordreset/request", \
        data=data, headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_non_registered_email_request():
    """
    Pytest function to test non registered email being entered into the function
    - The user should not get reset_code successfully, InputError should be thrown
    """
    # reset the workspace
    reset_workspace()

    # normal email
    data = json.dumps({
        "email": 'jay.chen@gmail.com'
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/passwordreset/request", \
        data=data, headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_auth_password_request_normal():
    """
    Pytest function to test request password reset successfully
    - The user should request successfully and get the reset code by email
    Input: JSON - {email}
    output: JSON - {}
    """
    # reset the workspace
    reset_workspace()

    # registered user
    data = json.dumps({
        "email": 'jay.chen@gmail.com',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req1)

    # normal email
    data = json.dumps({
        "email": 'jay.chen@gmail.com'
    }).encode('utf-8')

    req2 = urllib.request.Request(f"{BASE_URL}/auth/passwordreset/request", \
        data=data, headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    urllib.request.urlopen(req2)

def test_passwordreset_invalid_code():
    """
    Function use invalid reset_code to reset the newpassowrd
    - The password should not reset successfully, InputError should be thrown
    """
    reset_workspace()

    # registered user
    data = json.dumps({
        "email": 'jay.chen@gmail.com',
        "password": '123456',
        "name_first": 'Jay',
        "name_last": 'Chen'
    }).encode('utf-8')

    req1 = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req1)

    # normal email
    data = json.dumps({
        "email": 'jay.chen@gmail.com'
    }).encode('utf-8')

    req2 = urllib.request.Request(f"{BASE_URL}/auth/passwordreset/request", \
        data=data, headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    urllib.request.urlopen(req2)

    # invalid  reset_code and normal password
    data = json.dumps({
        "reset_code": 'INVALID',
        "new_password": "abc12345"
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/passwordreset/reset", \
        data=data, headers={'Content-Type': 'application/json'})
    # response = urllib.request.urlopen(req)
    # payload = json.load(response)
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
