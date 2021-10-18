#pylint: disable=R0801
"""
 Test program for testing user_profile_sethandle function in Slackr (COMP1531 major project)
 Written by Robert Teoh for team JRKS1531

 Assumptions:
   Assumes that auth_register is functioning correctly.
   Assumes that user_profile is functioning correctly.
   Assumes that 「0」 (integer) is not a valid token.
"""

###################################
# Error conditions (Error will occur if):
#   handle_str is not between 3 and 20 characters   ->   InputError
#   Handle is already in use by another user        ->   InputError
#
#
# Function call syntax:
#   user_profile_sethandle(token, handle_str)
#
# (Returns nothing. Sets the handle of the token-authenticated user.)
####################################

import pytest
from user import user_profile_sethandle, user_profile
from auth import auth_register
from error import InputError, AccessError
from server_data_class import Server_data

#Create test user 1 (Jessica)
def generate_user_1(server_data):
    """
    Creates a example/test user using auth_register.
    """
    user_1_details = auth_register(server_data, "jess@test.com", "ABC1234", "Jessica", "Wu")
    return user_1_details
    #Handle for this user is "jessicawu"

#Create test user 2 (Patrick)
def generate_user_2(server_data):
    """
    Creates a example/test user using auth_register.
    """
    user_2_details = auth_register(server_data, "patrick@test.com", "ABC7890", "Patrick", "Macalin")
    return user_2_details
    #Handle for this user is "patrickmacalindong"


def test_normal():
    """
    Normal test, with valid data only.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "testhandle1234"

    #Check whether the function call succeeds.
    assert user_profile_sethandle(server_data, user_1_token, handle_str) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "testhandle1234"

def test_min():
    """
    Normal test, with valid data only.
    Handle to test is minimum length.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "tes" #3 chars (minimum length)

    #Check whether the function call succeeds.
    assert user_profile_sethandle(server_data, user_1_token, handle_str) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "tes"

def test_max():

    """
    Normal test, with valid data only.
    Handle to test is maximum length.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "thisnameismaxlengthA" #20 chars (maximum length)

    #Check whether the function call succeeds.
    assert user_profile_sethandle(server_data, user_1_token, handle_str) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "thisnameismaxlengthA"

def test_invalid_token():
    """
    Tests with invalid token and valid handle.
    AccessError will occur due to invalid token.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    test_token = '0'

    handle_str = "aaaa"
    #AccessError will occur as the token is not valid.
    with pytest.raises(AccessError):
        user_profile_sethandle(server_data, test_token, handle_str)

    #Verify that the handle was not set.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "jessicawu"

def test_empty_token():
    """
    Tests with invalid (empty) token and valid handle.
    AccessError will occur due to invalid token.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    test_token = ''

    handle_str = "aaaa" #1 char (below minimum length)

    #AccessError will occur as the token is not valid.
    with pytest.raises(AccessError):
        user_profile_sethandle(server_data, test_token, handle_str)

    #Verify that the handle was not set.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "jessicawu"

def test_too_short():
    """
    Tests with valid token and invalid handle (too short).
    InputError will occur because handle-is-not-valid.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "a" #1 char (below minimum length)

    #InputError will occur as the handle is too short.
    with pytest.raises(InputError):
        user_profile_sethandle(server_data, user_1_token, handle_str)

    #Verify that the handle was not set.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "jessicawu"

def test_too_long():
    """
    Tests with valid token and invalid handle (too long).
    InputError will occur because handle-is-not-valid.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "thishandleistoolongandnotvalid" #30 chars (too long)

    #InputError will occur as the handle is too long.
    with pytest.raises(InputError):
        user_profile_sethandle(server_data, user_1_token, handle_str)

    #Verify that the handle was not set.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "jessicawu"

def test_1_above_maximum():
    """
    Tests with valid token and invalid handle (too long).
    InputError will occur because handle-is-not-valid.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "thishandleistoolongAA" #21 chars (above maximum length)

    #InputError will occur as the handle is too long.
    with pytest.raises(InputError):
        user_profile_sethandle(server_data, user_1_token, handle_str)

    #Verify that the handle was not set.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["handle_str"] == "jessicawu"

def test_handle_already_taken():
    """
    Tests with valid token and handle that is already in use.
    InputError will occur due to handle-already-in-use.
    """

    server_data = Server_data()

    #Generate user 1 (Jessica) with automatically generated handle "jessicawu"
    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    handle_str = "jessicawu"

    #Generate user 2 (Patrick) for second call
    user_2 = generate_user_2(server_data)
    user_2_token = user_2["token"]
    user_2_id = user_2["u_id"]

    #Attempt to assign the same handle to a different user.

    #InputError will occur as the handle is already in use.
    with pytest.raises(InputError):
        user_profile_sethandle(server_data, user_2_token, handle_str)

    #Verify that neither user (User 1 and 2) were not affected by the previous
    #attempt to set an already-in-use handle to a different user.
    updated_user_1 = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user_1["user"]["handle_str"] == "jessicawu"

    updated_user_2 = user_profile(server_data, user_2_token, user_2_id)
    assert updated_user_2["user"]["handle_str"] == "patrickmacalin"
