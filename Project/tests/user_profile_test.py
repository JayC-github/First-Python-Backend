#pylint: disable=R0801
"""
Test program for users_profile function in Slackr (COMP1531 major project)
Written by Robert Teoh for team JRKS1531

Assumptions:
    Assumes that auth_register is functioning correctly.
    Assumes that 「0」(zero, int) is not a valid value for a token.

Error conditions:
    Token is not valid (AccessError)
    u_id is not valid / user does not exist (InputError)

###################################
# Function call syntax:
#   user_profile(token, u_id)
#
# (For a valid user, returns information about their email, first name, last name, and handle)
###################################
"""


import pytest
from user import user_profile
from auth import auth_register
from error import InputError, AccessError

from server_data_class import Server_data

#Helper functions to create test users
def generate_user_id_1(server_data):
    """
    Creates a test/example user.
    """
    user_1_details = auth_register(server_data, "jess@test.com", "ABC1234", "Jessica", "Wu")
    return user_1_details["u_id"]

def generate_user_id_2(server_data):
    """
    Creates a test/example user.
    """
    user_2_details = auth_register(server_data, "patrick@test.com", "ABC7890", "Patrick", "Chen")
    return user_2_details["u_id"]

def generate_user_id_3(server_data):
    """
    Creates a test/example user.
    """
    user_3_details = auth_register(server_data, "brandon@test.com", "ABC4321", "Brandon", "Ho")
    return user_3_details["u_id"]

def generate_user_id_4(server_data):
    """
    Creates a test/example user.
    """
    user_4_details = auth_register(server_data, "chloe@test.com", "ABC9876", "Chloe", "Chan")
    return user_4_details["u_id"]

def generate_user_id_5(server_data):
    """
    Creates a test/example user.
    """
    user_5_details = auth_register(server_data, "tim@test.com", "ABC3456", "Tim", "Zhang")
    return user_5_details["u_id"]


#Helper function to generate 1 user with a known/recorded token
# (token which will be used to test the function)
def generate_user_6(server_data):
    """
    Creates a test/example user.
    """
    user_6_details = auth_register(server_data, "isabella@test.com", "ABC4567", "Isabella", "Ning")
    return user_6_details

#Tests user_profile with a valid token, querying the data of 1 user (among 6) only.
def test_valid_token_single():
    """
    Tests user_profile with a valid token, querying the data of 1 user (among 6) only.
    """
    server_data = Server_data()

    #Generate 5 users and collect their user ID
    user_1_id = generate_user_id_1(server_data)

    generate_user_id_2(server_data)
    generate_user_id_3(server_data)
    generate_user_id_4(server_data)
    generate_user_id_5(server_data)

    #Generate 1 additional user and collect their user ID and token
    user_6_details = generate_user_6(server_data)
    user_6_token = user_6_details["token"]

    #Test the function with user 6's token
    #Query for user 1's profile.
    assert user_profile(server_data, user_6_token, user_1_id)["user"] == {
        'u_id': user_1_id,
        'email': 'jess@test.com',
        'name_first': 'Jessica',
        'name_last': 'Wu',
        'handle_str': 'jessicawu',
        'profile_img_url': ''
    }

#Tests user_profile with a valid token, querying the data of all 6 users.
def test_valid_token_multiple():
    """
    Tests user_profile with a valid token, querying the data of all 6 users.
    """
    server_data = Server_data()

    #Generate 5 users and collect their user ID
    user_1_id = generate_user_id_1(server_data)
    user_2_id = generate_user_id_2(server_data)
    user_3_id = generate_user_id_3(server_data)
    user_4_id = generate_user_id_4(server_data)
    user_5_id = generate_user_id_5(server_data)

    #Generate 1 additional user and collect their user ID and token
    user_6_details = generate_user_6(server_data)
    user_6_id = user_6_details["u_id"]
    user_6_token = user_6_details["token"]

    #Test the function with user 6's token
    #Query for user 1's profile.
    assert user_profile(server_data, user_6_token, user_1_id)["user"] == {
        'u_id': user_1_id,
        'email': 'jess@test.com',
        'name_first': 'Jessica',
        'name_last': 'Wu',
        'handle_str': 'jessicawu',
        'profile_img_url': ''
    }

    #Test the function with user 6's token
    #Query for user 2's profile.
    assert user_profile(server_data, user_6_token, user_2_id)["user"] == {
        'u_id': user_2_id,
        'email': 'patrick@test.com',
        'name_first': 'Patrick',
        'name_last': 'Chen',
        'handle_str': 'patrickchen',
        'profile_img_url': ''
    }

    #Test the function with user 6's token
    #Query for user 3's profile.
    assert user_profile(server_data, user_6_token, user_3_id)["user"] == {
        'u_id': user_3_id,
        'email': 'brandon@test.com',
        'name_first': 'Brandon',
        'name_last': 'Ho',
        'handle_str': 'brandonho',
        'profile_img_url': ''
    }

    #Test the function with user 6's token
    #Query for user 4's profile.
    assert user_profile(server_data, user_6_token, user_4_id)["user"] == {
        'u_id': user_4_id,
        'email': 'chloe@test.com',
        'name_first': 'Chloe',
        'name_last': 'Chan',
        'handle_str': 'chloechan',
        'profile_img_url': ''
    }

    #Test the function with user 6's token
    #Query for user 5's profile.
    assert user_profile(server_data, user_6_token, user_5_id)["user"] == {
        'u_id': user_5_id,
        'email': 'tim@test.com',
        'name_first': 'Tim',
        'name_last': 'Zhang',
        'handle_str': 'timzhang',
        'profile_img_url': ''
    }

    #Test the function with user 6's token
    #Query for user 6's profile.
    assert user_profile(server_data, user_6_token, user_6_id)["user"] == {
        'u_id': user_6_id,
        'email': 'isabella@test.com',
        'name_first': 'Isabella',
        'name_last': 'Ning',
        'handle_str': 'isabellaning',
        'profile_img_url': ''
    }

#Tests user_profile with an invalid token, querying the data of all 6 users.
def test_invalid_token_multiple():
    """
    Tests user_profile with an invalid token, querying the data of all 6 users.

    AccessError should occur due to invalid token.
    """
    server_data = Server_data()

    #Generate 5 users and collect their user ID
    user_1_id = generate_user_id_1(server_data)
    user_2_id = generate_user_id_2(server_data)
    user_3_id = generate_user_id_3(server_data)
    user_4_id = generate_user_id_4(server_data)
    user_5_id = generate_user_id_5(server_data)

    #Generate 1 additional user and collect their user ID and token
    user_6_details = generate_user_6(server_data)
    user_6_id = user_6_details["u_id"]

    token = 0

    #Test the function with invalid token
    #Query for user 1's profile.
    with pytest.raises(AccessError):
        user_profile(server_data, token, user_1_id)

    #Test the function with invalid token
    #Query for user 2's profile.
    with pytest.raises(AccessError):
        user_profile(server_data, token, user_2_id)

    #Test the function with invalid token
    #Query for user 3's profile.
    with pytest.raises(AccessError):
        user_profile(server_data, token, user_3_id)

    #Test the function with invalid token
    #Query for user 4's profile.
    with pytest.raises(AccessError):
        user_profile(server_data, token, user_4_id)

    #Test the function with invalid token
    #Query for user 5's profile.
    with pytest.raises(AccessError):
        user_profile(server_data, token, user_5_id)

    #Test the function with invalid token
    #Query for user 6's profile.
    with pytest.raises(AccessError):
        user_profile(server_data, token, user_6_id)

#Attempts to find the data for a user that does not exist.
#Uses a valid token.
#Tests user_profile with an invalid token, querying the data of all 6 users.
def test_valid_token_invalid_id():
    """
    Attempts to find the data for a user that does not exist.
    Uses a valid token.
    Tests user_profile with an invalid token, querying the data of all 6 users.

    InputError should occur due to invalid user ID.
    """
    server_data = Server_data()

    #Generate 5 users and collect their user ID
    user_1_id = generate_user_id_1(server_data)
    user_2_id = generate_user_id_2(server_data)
    user_3_id = generate_user_id_3(server_data)
    user_4_id = generate_user_id_4(server_data)
    user_5_id = generate_user_id_5(server_data)

    #Generate 1 additional user and collect their user ID and token
    user_6_details = generate_user_6(server_data)
    user_6_id = user_6_details["u_id"]
    user_6_token = user_6_details["token"]

    #Generate a random number as the ID to query and ensure
    #that there is no user with that ID.
    test_id = 123
    id_exists = True

    while id_exists:
        #Check whether the ID is the ID of a valid user.
        id_exists = False
        if test_id == user_1_id or test_id == user_2_id or test_id == user_3_id:
            id_exists = True
        if test_id == user_4_id or test_id == user_5_id or test_id == user_6_id:
            id_exists = True

        #If the ID to test is actually the ID of a valid user, change it (by adding 1).
        if id_exists:
            test_id += 1

    #Test the function with user 6's token
    #Query for the profile of a nonexistent user (There is no user with the specified ID).

    #InputError will occur because
    #   User with u_id is not a valid user
    with pytest.raises(InputError):
        user_profile(server_data, user_6_token, test_id)

#Attempts to find the data for a user that does not exist.
#Uses an invalid token.
#Tests user_profile with an invalid token, querying the data of all 6 users.
def test_invalid_token_invalid_id():
    """
    Attempts to find the data for a user that does not exist.
    Uses an invalid token.
    Tests user_profile with an invalid token, querying the data of all 6 users.

    AccessError should occur due to invalid token.
    """
    server_data = Server_data()

    #Generate 5 users and collect their user ID
    user_1_id = generate_user_id_1(server_data)
    user_2_id = generate_user_id_2(server_data)
    user_3_id = generate_user_id_3(server_data)
    user_4_id = generate_user_id_4(server_data)
    user_5_id = generate_user_id_5(server_data)

    #Generate 1 additional user and collect their user ID and token
    user_6_details = generate_user_6(server_data)
    user_6_id = user_6_details["u_id"]

    #Invalid token.
    token = 0

    #Generate a random number as the ID to query and ensure
    #that there is no user with that ID.
    test_id = 123
    id_exists = True

    while id_exists:
        #Check whether the ID is the ID of a valid user.
        id_exists = False
        if test_id == user_1_id or test_id == user_2_id or test_id == user_3_id:
            id_exists = True
        if test_id == user_4_id or test_id == user_5_id or test_id == user_6_id:
            id_exists = True

        #If the ID to test is actually the ID of a valid user, change it (by adding 1).
        if id_exists:
            test_id += 1

    #Test the function with user 6's token
    #Query for the profile of a nonexistent user (There is no user with the specified ID).

    #AccessError will occur because
    #   Token is not valid.
    with pytest.raises(AccessError):
        user_profile(server_data, token, test_id)
