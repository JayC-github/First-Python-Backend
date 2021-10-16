#pylint: disable=R0801
"""
Test program for user_profile_setname function in Slackr (COMP1531 major project)
Written by Robert Teoh for team JRKS1531

Assumptions:
    Assumes that auth_register is functioning correctly.
    Assumes that 「0」(zero, int) is not a valid value for a token.
"""
###################################
#   Error conditions (Error will occur if):
#       Token is not valid                          ->     AccessError
#       name_first not between 1-50 chars length    ->     InputError
#       name_last  not between 1-50 chars length    ->     InputError
#
#
#   Function call syntax:
#       user_profile_setname(token, name_first, name_last)
###################################

import pytest
from user import user_profile_setname, user_profile
from auth import auth_register
from error import InputError, AccessError

from server_data_class import Server_data


#Create test user 1 (Jessica)
def generate_user_1(server_data):
    """
    Creates a test/example user.
    """
    user_1_details = auth_register(server_data, "jess@testdomain.com", "ABC1234", "Jessica", "Wu")
    return user_1_details


#Test cases below.

def test_normal():
    """
    Normal test case.
    Attempts to set the name to a name that is valid.

    Verifies that the user details were successfully updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "testfirstname"
    name_last = "testlastname"

    #Check whether the function call succeeds.
    assert user_profile_setname(server_data, user_1_token, name_first, name_last) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "testfirstname"
    assert updated_user["user"]["name_last"] == "testlastname"


def test_long_names_50():
    """
    Normal test case.
    Attempts to set the name to a name that is long but valid.

    Verifies that the user details were successfully updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "ThisIsAValidFirstNameThatIsVeryLongForTestPurposes"   #50 chars in length
    name_last = "ThisIsAValidLastNameThatIsVeryLongForTestPurposesA"    #50 chars in length

    #This should work but this is at the upper limit of the name length (50 chars).

    #Check whether the function call succeeds.
    assert user_profile_setname(server_data, user_1_token, name_first, name_last) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == name_first
    assert updated_user["user"]["name_last"] == name_last


def test_too_long():
    """
    Attempts to set the names to a name that is too long

    InputError should occur.
    Verifies that the user details were not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "ThisIsAnInvalidFirstNameThatIsTooLongForTestPurposesItShouldNotWork"  #67 chars
    name_last = "ThisIsAnInvalidLastNameThatIsTooLongForTestPurposesItShouldNotWork"    #66 chars

    #InputError will occur because
    #   name_first is not between 1-50 chars in length (67 chars - too many)
    #   name_last is not between 1-50 chars in length  (66 chars - too many)

    with pytest.raises(InputError):
        user_profile_setname(server_data, user_1_token, name_first, name_last)

    #Verify that the name was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "Jessica"
    assert updated_user["user"]["name_last"] == "Wu"


def test_short():
    """
    Attempts to set the names to a name that is too short

    InputError should occur.
    Verifies that the user details were not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "f"    #1 char in length
    name_last = "l"     #1 char in length

    #This should work but this is at the lower limit of the name length (1 char).

    #Check whether the function call succeeds.
    assert user_profile_setname(server_data, user_1_token, name_first, name_last) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "f"
    assert updated_user["user"]["name_last"] == "l"


def test_empty():
    """
    Attempts to set the name to a name that is empty.

    InputError should occur.
    Verifies that the user details were not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = ""
    name_last = ""

    #InputError will occur because
    #   name_first is not between 1-50 chars in length (0 chars - too few)
    #   name_last is not between 1-50 chars in length  (0 chars - too few)
    with pytest.raises(InputError):
        user_profile_setname(server_data, user_1_token, name_first, name_last)

    #Verify that the name was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "Jessica"
    assert updated_user["user"]["name_last"] == "Wu"


def test_invalid_token():
    """
    Attempts to set the name to a name that is valid
    with an invalid token.

    AccessError should occur.
    Verifies that the user details were not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_id = user_1["u_id"]

    #Set an invalid token.
    token = 0

    name_first = "testfirstname"
    name_last = "testlastname"

    #InputError will occur because the token is not valid.
    with pytest.raises(AccessError):
        user_profile_setname(server_data, token, name_first, name_last)

    #Set token to valid token
    token = user_1["token"]

    #Verify that the name was not updated.
    updated_user = user_profile(server_data, token, user_1_id)
    assert updated_user["user"]["name_first"] == "Jessica"
    assert updated_user["user"]["name_last"] == "Wu"


def test_missing_first():
    """
    Attempts to set the first name to a name that is empty.

    InputError should occur.
    Verifies that the user details were not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = ""
    name_last = "testlastname"

    #InputError will occur because
    #   name_first is not between 1-50 chars in length (0 chars)
    with pytest.raises(InputError):
        user_profile_setname(server_data, user_1_token, name_first, name_last)

    #Verify that the name was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "Jessica"
    assert updated_user["user"]["name_last"] == "Wu"


def test_missing_last():
    """
    Attempts to set the last name to a name that is empty.

    InputError should occur.
    Verifies that the user details were not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "testfirstname"
    name_last = ""

    #InputError will occur because
    #   name_last is not between 1-50 chars in length (0 chars)
    with pytest.raises(InputError):
        user_profile_setname(server_data, user_1_token, name_first, name_last)

    #Verify that the name was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "Jessica" #The name was set in the fixture.
    assert updated_user["user"]["name_last"] == "Wu" #The name was set in the fixture.


def test_numbers():
    """
    Attempts to set the name to a valid name composed of numbers.

    Verifies that the user details were successfully updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "12341234"
    name_last = "45674567"

    #This should still be considered a valid input.

    #Check whether the function call succeeds.
    assert user_profile_setname(server_data, user_1_token, name_first, name_last) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "12341234"
    assert updated_user["user"]["name_last"] == "45674567"


def test_symbols():
    """
    Attempts to set the name to a valid name composed of symbols.

    Verifies that the user details were successfully updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    name_first = "!@#$%^&*();+-_"
    name_last = "+_)(*&^%$#@"

    #This should still be considered a valid input.

    #Check whether the function call succeeds.
    assert user_profile_setname(server_data, user_1_token, name_first, name_last) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["name_first"] == "!@#$%^&*();+-_"
    assert updated_user["user"]["name_last"] == "+_)(*&^%$#@"
