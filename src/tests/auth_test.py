#pylint: disable=R0801,W0105,W0611,W0612
"""
auth_test.py
"""
import pytest
from error import InputError, AccessError
from auth import auth_register, auth_login, auth_logout, \
auth_passwordreset_request, auth_passwordreset_reset
from user import user_profile
from server_data_class import Server_data
from sessions_class import Sessions
"""
1.tests for auth_register

Input Error
- Email entererd is not valid
- Email address is already being used by another user
- password entered is less than 6 characters long
- name first is not between 1-50 characters in length
- name last is not between 1-50 characters in length

# A handle is generated that is the concatentation of a lowercase-only
# first name and last name.
# If the concatenation is longer than 20 characters, it is cutoff at 20
# characters.
# If the handle is already taken, modify the handle to make it unique

"""
def test_register():
    """
    registration success
    """
    server_data = Server_data()
    email = "jay.chen@unsw.edu.au"
    # assert check(email) == True
    user = auth_register(server_data, email, "abcde123", "Jay", "Chen")
    user_id = user['u_id']
    token = user['token']

    # assume the token is generated from using auth_register
    # check the handle
    assert user_profile(server_data, token, user_id) == {
        'user': {\
            'u_id': user_id, \
        	'email': 'jay.chen@unsw.edu.au', \
        	'name_first': 'Jay', \
        	'name_last': 'Chen', \
        	'profile_img_url': '', \
        	'handle_str': 'jaychen', \
        },
    }

    email2 = "mercy.duong@unsw.edu.au"
    user2 = auth_register(server_data, email2, "123abc", "Jay", "Chen")
    user_id2 = user2['u_id']
    token2 = user2['token']

    # assume the token is generated from using auth_register
    # check the handle
    assert user_profile(server_data, token2, user_id2) == {
        'user': {\
            'u_id': user_id2, \
        	'email': 'mercy.duong@unsw.edu.au', \
        	'name_first': 'Jay', \
        	'name_last': 'Chen', \
        	'profile_img_url': '', \
        	'handle_str': '1jaychen', \
        },
    }

def test_register_handle():
    """
    registration success with len(first name + last name) > 20
    handle cutoff at 20 characters
    """
    server_data = Server_data()
    email = "jay.chen@unsw.edu.au"
    # assert check(email) == True
    user = auth_register(server_data, email, "abcde123", "J"*25, "Chen")
    user_id = user['u_id']
    token = user['token']

    # assume the token is generated from using auth_register
    # check the handle
    # handle should be cutoff at the 20th characters
    assert user_profile(server_data, token, user_id) == {
        'user': {\
        	'u_id': user_id, \
        	'email': 'jay.chen@unsw.edu.au', \
        	'name_first': 'J' * 25, \
        	'name_last': 'Chen', \
        	'profile_img_url': '', \
        	'handle_str': 'j' * 20, \
        },
    }

def test_register_valid_email():
    """
    Email entererd is not valid
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_register(server_data, "jay.chen", "abcde123", "Jay", "Chen")

def test_register_double():
    """
    Email address is already being used by another user
    """
    server_data = Server_data()
    email = "jay.chen@unsw.edu.au"
    user = auth_register(server_data, email, "abcde123", "Jay", "Chen")

    # try to register by using the same email address
    with pytest.raises(InputError):
        auth_register(server_data, email, "abcde456", "Jacky", "Chan")

def test_register_short_password():
    """
    password entered is less than 6 characters long
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_register(server_data, "jay.chen@unsw.edu.au", "ab12", "Jay", "Chen")

def test_register_first_name():
    """
    # first name is not between 1-50 characters in length
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_register(server_data, "jay.chen@unsw.edu.au", "abc123", "J" * 51, "Chen")

def test_register_first_name_empty():
    """
    first name empty
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_register(server_data, "jay.chen@unsw.edu.au", "abc123", "", "Chen")

def test_register_last_name():
    """
    # last name is not between 1-50 characters in length
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_register(server_data, "jay.chen@unsw.edu.au", "abc123", "Jay", "C" * 51)

def test_register_last_name_empty():
    """
    last name empty
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_register(server_data, "jay.chen@unsw.edu.au", "abc123", "Jay", "")

"""
2.tests for auth_login

Input Error
- Email entererd is not valid
- Email entered does not belong to a user
- password is not correct

"""
def test_login():
    """
    # login successfully
    """
    server_data = Server_data()
    result1 = auth_register(server_data, "jay.chen@unsw.edu.au", "abcde123", "Jay", "Chen")
    u_id1 = result1['u_id']
    token1 = result1['token']

    # the registered user login
    result2 = auth_login(server_data, "jay.chen@unsw.edu.au", "abcde123")
    u_id2 = result2['u_id']
    token2 = result2['token']

    # the user id should be the same but tokens are unique & different
    assert u_id1 == u_id2
    assert token1 != token2

def test_login_valid_email():
    """
    # Email entered is not a valid email
    """
    server_data = Server_data()
    auth_register(server_data, "jay.chen@unsw.edu.au", "abcde123", "Jay", "Chen")
    with pytest.raises(InputError):
        auth_login(server_data, "jay.chen", "abcde123")

def test_login_user_email():
    """
    # Email entered does not belong to a user
    """
    server_data = Server_data()
    auth_register(server_data, "jay.chen@unsw.edu.au", "abcde123", "Jay", "Chen")
    # try to login with another random email
    with pytest.raises(InputError):
        auth_login(server_data, "MercyluvJay@gmail.com", "1234abc")

def test_login_password():
    """
    # password is not correct
    """
    server_data = Server_data()
    auth_register(server_data, "jay.chen@unsw.edu.au", "abcde123", "Jay", "Chen")
    # try to login with incorrect password
    with pytest.raises(InputError):
        auth_login(server_data, "jay.chen@unsw.edu.au", "2384u2ekjh28")
"""
3. tests for auth_logout
- Invalid token (logout before login)
- Double logout
"""
def test_logout():
    """
    # logout successfully
    # user registers successfully->login automatically
    """
    server_data = Server_data()
    user = auth_register(server_data, "jay.chen@unsw.edu.au", "abcde123", "Jay", "Chen")
    user_login = auth_login(server_data, "jay.chen@unsw.edu.au", "abcde123")

    token1 = user['token']
    token2 = user_login['token']

    assert auth_logout(server_data, token1) == {'is_success': True}
    assert auth_logout(server_data, token2) == {'is_success': True}

def test_invalid_log_out():
    """
    # logout after logout/ logout before login
    """
    server_data = Server_data()
    user = auth_register(server_data, "jay.chen@unsw.edu.au", "abcde123", "Jay", "Chen")
    auth_login(server_data, "jay.chen@unsw.edu.au", "abcde123")
    token = user['token']

    # logout the user first
    assert auth_logout(server_data, token) == {'is_success': True}

    # already logout, this token should be invalid, cannot logout again
    # or logout before login
    assert auth_logout(server_data, token) == {'is_success': False}

"""
4. tests for auth_password_request
"""
def test_auth_passwordreset_request():
    """
    After using password request user should get a reset_code
    """
    server_data = Server_data()
    email = "jianjunjchen@gmail.com"
    # assert check(email) == True
    user = auth_register(server_data, email, "abcde123", "Jay", "Chen")
    user_id = user['u_id']
    token = user['token']

    # assume the token is generated from using auth_register
    assert user_profile(server_data, token, user_id) == {
        'user': {\
            'u_id': user_id, \
        	'email': "jianjunjchen@gmail.com", \
        	'name_first': 'Jay', \
        	'name_last': 'Chen', \
        	'profile_img_url': '', \
        	'handle_str': 'jaychen', \
        },
    }
    # get the user's full information by email
    # reset code should be empty
    user_full = server_data.get_user_by_email(email)
    assert user_full.reset_code == ""

    # request to set a new password, will get a reset_code
    # after request send, user receive a secret reset_code
    auth_passwordreset_request(server_data, email)
    assert user_full.reset_code != ""

def test_auth_reset_invalid_email():
    """
    use a invalid email to request a password reset
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_passwordreset_request(server_data, "jay.chen")

def test_auth_reset_no_email():
    """
    use an non registered email to request a password reset
    """
    server_data = Server_data()
    with pytest.raises(InputError):
        auth_passwordreset_request(server_data, "jay.mercy@gmail.com")
"""
5.tests for auth_password_reset

Input Error
- reset_code entererd is not valid
- newpassword is not valid

"""
def test_auth_passwordreset_reset():
    """
    password entered is less than 6 characters long
    """
    server_data = Server_data()
    email = "jianjunjchen@gmail.com"

    auth_register(server_data, email, "abcde123", "Jay", "Chen")
    # get the user's full information by email
    # reset code should be empty
    user_full = server_data.get_user_by_email(email)
    old_password = user_full.password
    assert user_full.reset_code == ""

    # request to set a new password, will get a reset_code
    # after request send, user receive a secret reset_code
    auth_passwordreset_request(server_data, email)
    reset_code = user_full.reset_code
    assert reset_code != ""

    # reset the password by using valid code
    auth_passwordreset_reset(server_data, reset_code, "1234abc")

    # check if the password has change to the new one
    new_password = user_full.password
    assert new_password != old_password

def test_reset_code_invalid():
    """
    password entered is less than 6 characters long
    """
    server_data = Server_data()
    email = "jianjunjchen@gmail.com"

    auth_register(server_data, email, "abcde123", "Jay", "Chen")
    # get the user's full information by email
    # reset code should be empty
    user_full = server_data.get_user_by_email(email)
    assert user_full.reset_code == ""

    # request to set a new password, will get a reset_code
    # after request send, user receive a secret reset_code
    auth_passwordreset_request(server_data, email)
    reset_code = user_full.reset_code
    assert reset_code != ""

    with pytest.raises(InputError):
        auth_passwordreset_reset(server_data, "invalid_code", "abcde1234")



def test_reset_password_short():
    """
    password entered is less than 6 characters long
    """
    server_data = Server_data()
    email = "jianjunjchen@gmail.com"

    auth_register(server_data, email, "abcde123", "Jay", "Chen")
    # get the user's full information by email
    # reset code should be empty
    user_full = server_data.get_user_by_email(email)
    assert user_full.reset_code == ""

    # request to set a new password, will get a reset_code
    # after request send, user receive a secret reset_code
    auth_passwordreset_request(server_data, email)
    reset_code = user_full.reset_code
    assert reset_code != ""

    with pytest.raises(InputError):
        auth_passwordreset_reset(server_data, reset_code, "abc")
