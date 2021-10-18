#pylint: disable=R0801
"""
Test program for users_all function in Slackr (COMP1531 major project)
Written by Robert Teoh for team JRKS1531

Assumptions:
   Assumes that auth_register is functioning correctly.
   Assumes that 「0」(zero, int) is not a valid value for a token.

###################################
# Function call syntax:
#   users_all(token)
#
# (Returns a list of all users and their associated details)
###################################
"""

import pytest
from user import users_all
from auth import auth_register
from error import AccessError

from server_data_class import Server_data


#Helper functions to create test users
def generate_user_id_1(server_data):
    """
    Creates a test/example user.
    """
    user_1 = auth_register(server_data, "jess@testdomain.com", "ABC1234", "Jessica", "Wu")
    return user_1["u_id"]

def generate_user_id_2(server_data):
    """
    Creates a test/example user.
    """
    user_2 = auth_register(server_data, "patrick@testdomain.com", "ABC7890", "Patrick", "Chen")
    return user_2["u_id"]

def generate_user_id_3(server_data):
    """
    Creates a test/example user.
    """
    user_3 = auth_register(server_data, "brandon@testdomain.com", "ABC4321", "Brandon", "Ho")
    return user_3["u_id"]

def generate_user_id_4(server_data):
    """
    Creates a test/example user.
    """
    user_4 = auth_register(server_data, "chloe@testdomain.com", "ABC9876", "Chloe", "Chan")
    return user_4["u_id"]

def generate_user_id_5(server_data):
    """
    Creates a test/example user.
    """
    user_5 = auth_register(server_data, "tim@testdomain.com", "ABC3456", "Tim", "Zhang")
    return user_5["u_id"]

#Setup function to generate 1 user with a known/recorded token
#(which will be used to test the function)
def generate_user_6(server_data):
    """
    Creates a test/example user. Returns the user ID and token.
    """
    user_6 = auth_register(server_data, "isabella@testdomain.com", "ABC4567", "Isabella", "Ning")
    return user_6


#Tests users_all with a valid token
def test_valid_token():
    """
    Tests users_all with a valid token, verifying the returned data.
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
    assert users_all(server_data, user_6_token) == {
        'users': [
            {
                'u_id': user_1_id,
                'email': 'jess@testdomain.com',
                'name_first': 'Jessica',
                'name_last': 'Wu',
                'handle_str': 'jessicawu',
                'profile_img_url': ''
            },

            {
                'u_id': user_2_id,
                'email': 'patrick@testdomain.com',
                'name_first': 'Patrick',
                'name_last': 'Chen',
                'handle_str': 'patrickchen',
                'profile_img_url': ''
            },

            {
                'u_id': user_3_id,
                'email': 'brandon@testdomain.com',
                'name_first': 'Brandon',
                'name_last': 'Ho',
                'handle_str': 'brandonho',
                'profile_img_url': ''
            },

            {
                'u_id': user_4_id,
                'email': 'chloe@testdomain.com',
                'name_first': 'Chloe',
                'name_last': 'Chan',
                'handle_str': 'chloechan',
                'profile_img_url': ''
            },

            {
                'u_id': user_5_id,
                'email': 'tim@testdomain.com',
                'name_first': 'Tim',
                'name_last': 'Zhang',
                'handle_str': 'timzhang',
                'profile_img_url': ''
            },

            {
                'u_id': user_6_id,
                'email': 'isabella@testdomain.com',
                'name_first': 'Isabella',
                'name_last': 'Ning',
                'handle_str': 'isabellaning',
                'profile_img_url': ''
            },
        ],
    }


#Tests users_all with no token
def test_no_token():
    """
    Tests users_all with an empty token.

    AccessError should occur due to invalid token.
    """
    server_data = Server_data()

    #Generate 6 users and collect their user ID
    generate_user_id_1(server_data)
    generate_user_id_2(server_data)
    generate_user_id_3(server_data)
    generate_user_id_4(server_data)
    generate_user_id_5(server_data)
    generate_user_6(server_data)

    #Create an empty token
    token = ""

    #Test the function with an empty token
    with pytest.raises(AccessError):
        users_all(server_data, token)

#Tests users_all with an invalid token
def test_invalid_token():
    """
    Tests users_all with an invalid token.

    AccessError should occur due to invalid token.
    """
    server_data = Server_data()

    #Generate 6 users
    generate_user_id_1(server_data)
    generate_user_id_2(server_data)
    generate_user_id_3(server_data)
    generate_user_id_4(server_data)
    generate_user_id_5(server_data)
    generate_user_6(server_data)

    test_token = 0

    #Test the function with an empty token
    with pytest.raises(AccessError):
        users_all(server_data, test_token)
