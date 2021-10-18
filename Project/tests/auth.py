"""re for the system"""
import re
import random
import hashlib
import string
import smtplib
from email.message import EmailMessage
import jwt
from error import InputError
# SMTP(simple mail transfer protocol)
#from json import dumps
#from flask import Flask, request
#import urllib.request

## file from group
#from server_data_class import Server_data
#from sessions_class import Sessions
# from user_class import User
# Secret for jwt(JSON Web Tokens) in python
# SECRET = "MERCY"

VALID_EMAIL = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

def generate_token(u_id):
    """
    return a new token for authenticaiton in users' session
    Input:
    - uid (integer)

    Output:
    - token(string)
    """
    # generate SECRET by using radom string--> len(random String) == 22
    letters = string.ascii_letters
    secret = ''.join(random.choice(letters) for i in range(22))
    return jwt.encode({'user_id': u_id}, secret, algorithm='HS256').decode('utf-8')

def auth_register(server_data, email, password, name_first, name_last):
    """
    auth_register function
    a function that create a new account for the user by given valid
    email, password and name

    Input:
    - server_data(obj)
    - email (string)
    - password (string)
    - name_first (string)
    - name_last (string)

    Output:
    - u_id (integer)
    - token (string)
    """
    # check if the email is valid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email enter is invalid")
    # check if the email address is alreayd being used by another user
    if server_data.does_email_exist(email):
        raise InputError("Email address is alreayd being used by another user")
    # check if the password entered is less than 6 characters long
    if len(password) < 6:
        raise InputError("Password is too short")
    # check if name first or name last is empty
    if not name_first:
        raise InputError("First name is empty")
    if not name_last:
        raise InputError("Last name is empty")
    # check if name first is not between 1-50 characters in length
    if len(name_first) > 50:
        raise InputError("first name is invalid")
    # check if name last is not between 1-50 characters in length
    if len(name_last) > 50:
        raise InputError("last name is invalid")
    # for the hash_password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # for the permission_id
    num = server_data.num_users()
    # for the very first user who signs up -- owners(1)
    if num == 0:
        permission_id = 1
    # all rest users are by default members(2)
    else:
        permission_id = 2

    # set handle here
    # if longer than 20 characters, handle is cutoff at 20 characters
    # handle can never be less than 2
    handle = (name_first + name_last).lower()
    handle = handle[:20]

    # if same handle is already exist
    # make handle unique by add user number in the front of the handle
    if server_data.does_handle_exist(handle):
        handle = str(num) + handle[:(20-len(str(num)))]

    # call the new_user fucntion to store in the database,return uid
    user_id = server_data.new_user(email, hashed_password, \
        name_first, name_last, handle, permission_id)

    # get the token by uid
    token = generate_token(user_id)

    # for session part
    session = server_data.get_sessions_list()
    session.create_active_session(user_id, token)

    return {'u_id': user_id, 'token': token}


def auth_login(server_data, email, password):
    """
    auth_login function
    Given a registered users' email and password and
    generates a valid token for the user to remain authenticated

    Inputs:
    - server_data(obj)
    - email (string)
    - password (string)

    Output:
    - u_id (integer)
    - token (string)
    """
    # check if the email is invalid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email enter is invalid")

    # check if the email is belong to a user
    # email not belong to a user
    if not server_data.does_email_exist(email):
        raise InputError("Email does not belong to a users")
    # email belong to a user
    else:
        # find the corresponding user's password and compare
        # password not match
        user = server_data.get_user_by_email(email)

        if user.password != hashlib.sha256(password.encode()).hexdigest():
            raise InputError("Password incorrect")
        # password match, return new token
        else:
            user_id = user.u_id
            token = generate_token(user_id)
            # for session part
            session = server_data.get_sessions_list()
            session.create_active_session(user_id, token)

            return {'u_id': user_id, 'token': token}

def auth_logout(server_data, token):
    """
    Given an active token, invalidates the taken to log the user out.
    If a valid token is given, and the user is successfully logged out,
    it returns true, otherwise false.

     Inputs:
    - server_data(obj)
    - token(string)

    Output:
    - True/False(string)
    """
    session = server_data.get_sessions_list()
    # if the token is valid
    if session.is_token_active(token):
        session.end_active_session(token)
        return {'is_success': True}
    return {'is_success': False}

def auth_passwordreset_request(server_data, email):
    """
    Given an email address of a registered user
    Send's them a an email containing a specific secret code- reset code
    for entered in auth_passwordreset_reset,
    User trying to reset the password is the one who got sent this email.

    input:
    - server_data(obj)
    - email (string)

    output:
    - {}
    """
    # check if the email is invalid
    if not re.search(VALID_EMAIL, email):
        raise InputError("Email enter is invalid")

    # check if the email is belong to a user
    # if email not belong to a user
    if not server_data.does_email_exist(email):
        raise InputError("Email does not belong to a users")
    # email belongs to a user, store the reset_code in this user
    else:
        user = server_data.get_user_by_email(email)
        mix = string.ascii_letters + string.digits
        code = ''.join(random.choice(mix) for i in range(20))
        user.reset_code = code

    # set the email server and send the 'reset_code' to the "email"
    address = "jrks1531@gmail.com"
    password = "jrks1531email"

    # set up the SMTP server
    setup = smtplib.SMTP(host='smtp.gmail.com', port=587)
    setup.starttls()
    setup.login(address, password)

    # create a message template
    msg = EmailMessage()
    msg['From'] = address
    msg['To'] = email
    msg['Subject'] = code

    setup.send_message(msg)
    setup.quit()
    return {}
    #return code
def auth_passwordreset_reset(server_data, reset_code, new_password):
    """
    Given a reset code for a user
    set that user's new password to the password provided

    input:
    - reset_code (string)
    - new_password(string)

    output:
    - {}
    """
    # reset_code is not a valid reset_code
    if not server_data.does_reset_code_exist(reset_code):
        raise InputError("Reset_code is invalid")
    # reset_code is valid, reset password
    else:
        # check if the new_password is invalid or not
        if len(new_password) < 6:
            raise InputError("Passowrd entered is not a valid password")
        else:
            user = server_data.get_user_by_reset_code(reset_code)
            user.password = new_password
    return {}
"""
if __name__ == "__main__":
    # Add two users
    server_data = Server_data()
    user1 = auth_register(server_data, "jayChen@gmail.com", "123456", "Jay", "Chen")
    u_id = user1['u_id']
    token = user1['token']
    #sessions = server_data.get_sessions_list()
    #sessions.create_active_session(u_id, token)

    print(user1)

    user2 = auth_login(server_data, "jayChen@gmail.com", "123456")
    u_id2 = user2['u_id']
    token2 = user2['token']
    #sessions = server_data.get_sessions_list()
    #sessions.create_active_session(u_id2, token2)

    print(user2)

    user3 = auth_register(server_data, "mercyDuong@gmail.com", "654321", "Mermer", "Duong")
    u_id3 = user3['u_id']
    token3 = user3['token']
    #sessions = server_data.get_sessions_list()
    #sessions.create_active_session(u_id3, token3)

    print(user3)

    message = auth_logout(server_data, token)
    print(message)
    message2 = auth_logout(server_data, token3)
    print(message2)
    message3 = auth_logout(server_data,token2)
    print(message3)
"""
