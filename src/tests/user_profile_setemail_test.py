#pylint: disable=R0801
"""
Test program for testing user_profile_setemail function in Slackr (COMP1531 major project)
Written by Robert Teoh for team JRKS1531

Assumptions:
    Assumes that auth_register is functioning correctly.
    Assumes that user_profile is functioning correctly.
    Assumes that 「0」 (zero) is not a valid token.
"""

###################################
#   Error conditions (Error will occur if):
#       Email is not valid                              ->   InputError
#
#       Email address is already in use by another user ->   InputError
#
#
#   Function call syntax:
#       user_profile_setemail(server_data, token, email)
####################################

import pytest
from user import user_profile_setemail, user_profile
from auth import auth_register
from error import InputError, AccessError

from server_data_class import Server_data

#Create test user 1 (Jessica)
def generate_user_1(server_data):
    """
    Creates a test/example user. Returns user ID and token.
    """
    user_1_details = auth_register(server_data, "jess@test.com", "ABC1234", "Jessica", "Wu")
    return user_1_details

#Create test user 2 (Patrick)
def generate_user_2(server_data):
    """
    Creates a test/example user. Returns user ID and token.
    """
    user_2_details = auth_register(server_data, "patrick@test.com", "ABC7890", "Patrick", "Chen")
    return user_2_details


#Test functions

#Normal test case. Uses valid email with 0 dots on LHS of '@' and 1 on RHS.
def test_normal_1():
    """
    Normal test case. All data inputs are valid.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "validtestemailaccount@testemaildomain.com"

    #Check whether the function call succeeds.
    assert user_profile_setemail(server_data, user_1_token, email) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "validtestemailaccount@testemaildomain.com"

#Normal test case. Uses valid email with 1 dot on LHS of '@' and 1 on RHS.
def test_normal_2():
    """
    Normal test case. All data inputs are valid.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "validtest1234.account@testemaildomain.com"

    #Check whether the function call succeeds.
    assert user_profile_setemail(server_data, user_1_token, email) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "validtest1234.account@testemaildomain.com"

#Normal test case. Uses valid email with symbols in the local part and
#dashes in the domain.
def test_normal_3():
    """
    Normal test case. All data inputs are valid.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "valid!#$%&'*+-/=?^_`{|}~account@test-email-domain.com"

    #Check whether the function call succeeds.
    assert user_profile_setemail(server_data, user_1_token, email) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "valid!#$%&'*+-/=?^_`{|}~account@test-email-domain.com"

#Attempts to set email with an invalid token.
def test_invalid_token():
    """
    Attempts to set email with an invalid token.
    An AccessError should occur as the token is not valid.
    """
    server_data = Server_data()

    token = 0

    email = "validtest.account@testemaildomain.com"

    #An AccessError should occur due to the invalid token.
    with pytest.raises(AccessError):
        user_profile_setemail(server_data, token, email)

#Attempts to set email with an empty token.
def test_empty_token():
    """
    Attempts to set email with an invalid token (empty token).
    An AccessError should occur as the token is not valid.
    """
    server_data = Server_data()

    token = ''

    email = "validtest.account@testemaildomain.com"

    #An AccessError should occur due to the invalid token.
    with pytest.raises(AccessError):
        user_profile_setemail(server_data, token, email)

#Missing '@' in email address. Test will produce an error.
def test_missing_at():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains no '@' character.

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccounttestemaildomain"

    #InputError will occur as email does not contain "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Two '@' characters in email address. Test will produce an error.
def test_double_at():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains 2 '@' characters.

    Verifies that the user email was not updated.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccounttestemaildomain"

    #InputError will occur as email does not contain "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Missing local part. Test will produce an error.
def test_missing_local():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains no local part (before '@').

    Verifies that the user email was not updated.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "@emaildomain.com"

    #InputError will occur as email does not contain "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Missing domain. Test will produce an error.
def test_missing_domain():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains no domain.

    Verifies that the user email was not updated.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "user1234@"

    #InputError will occur as email does not contain "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Local part contains only invalid characters.
def test_invalid_all_local_chars():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the local part contains contains "あ" (an invalid character).

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "あああああああ@testemaildomain.com"

    #InputError will occur as email contains "あ" (an invalid character).
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Domain contains only invalid characters ('あ').
def test_invalid_all_domain_chars_1():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the local part contains contains "あ" (an invalid character).

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "test@ああああ.あああ"

    #InputError will occur as email contains "あ" (an invalid character).
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Domain contains only invalid characters ('!').
def test_invalid_all_domain_chars_2():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the local part contains contains "!" (an invalid character).

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "test@!!!!.!!!"

    #InputError will occur as email contains "あ" (an invalid character).
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('あ') in the local part.
def test_invalid_char_in_local():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the local part contains contains "あ" (an invalid character).

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtあestemailaccount@testemaildomain.com"

    #InputError will occur as email contains "あ" (an invalid character).
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('あ') in the domain.
def test_invalid_char_in_domain_1():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the domain contains contains "あ" (an invalid character).

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount@testあemaildomain.com"

    #InputError will occur as domain contains "あ" (an invalid character).
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('!') in the domain. This char would be valid
#in the local part.
def test_invalid_char_in_domain_2():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the domain contains contains "!" (an invalid character).

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount@.test!emaildomain.com"

    #InputError will occur as domain contains "!" (an invalid character).
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('.') immediately before the "@".
def test_invalid_char_before_at_1():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains '.' immediately before '@'.

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount.@testemaildomain.com"

    #InputError will occur as email contains "." immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('-') immediately before the "@".
def test_invalid_char_before_at_2():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains '-' at the end of the local part.

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount-@testemaildomain.com"

    #InputError will occur as email contains "-" immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('.') immediately after the "@".
def test_invalid_char_after_at_1():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains '.' at the start of the domain.

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount@.testemaildomain.com"

    #InputError will occur as email contains "." immediately after "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('-') immediately after the "@".
def test_invalid_char_after_at_2():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email contains '-' at the start of the domain.

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount@-testemaildomain.com"

    #InputError will occur as email contains "-" immediately after "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('.') as first character.
def test_invalid_dot_as_first_char():
    """
    Tests with '.' as the first character. This is not valid.

    Verifies that error is thrown and user details did not change.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = ".invalid@testemaildomain.com"

    #InputError will occur as email contains "." immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('.') as last character in local part (before'@').
def test_invalid_dot_as_last_local_char():
    """
    Tests with '.' as the last character in the local part. This is not valid.

    Verifies that error is thrown and user details did not change.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalid.@testemaildomain.com"

    #InputError will occur as email contains "." immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character combination ('..') before the "@".
def test_invalid_double_dot_before_at():
    """
    Tests with two consecutive dots before '@'.

    Verifies that error is thrown and user details did not change.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalid..testemailaccount@testemaildomain.com"

    #InputError will occur as email contains "." immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character combination ('..') after the "@".
def test_invalid_double_dot_after_at():
    """
    Tests with two consecutive dots after '@'.

    Verifies that error is thrown and user details did not change.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtestemailaccount@testemail..domain.com"

    #InputError will occur as email contains "." immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid character ('.') immediately before and after the "@".
def test_invalid_double_dot_both_sides():
    """
    Tests with two consecutive dots on either side of '@'.

    Verifies that error is thrown and user details did not change.
    """

    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "invalidtest..emailaccount@testemail..domain.com"

    #InputError will occur as email contains "." immediately before "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Invalid email: no dot anywhere after "@",
def test_no_dot_after_at():
    """
    Attempts to set the email to an invalid email.
    InputError should occur as the email domain contains no '.' character.

    Verifies that the user email was not updated.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "emailwithnodot@testemaildomaincom"

    #InputError will occur as email does not contain "." anywhere after "@".
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that the email address was not updated.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "jess@test.com"

#Tests a valid email which has multiple '.' characters after the '@'.
def test_multiple_dots_after_at():
    """
    Normal test case.
    Multiple dots in acceptable poisitons in the domain.

    Verifies that the email is updated successfully.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "multipledotsindomain@valid.domain.edu.au"

    #Check whether the function call succeeds.
    assert user_profile_setemail(server_data, user_1_token, email) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "multipledotsindomain@valid.domain.edu.au"

#Tests a valid email which has multiple '.' characters before and after the '@'.
def test_multiple_dots_both_sides():
    """
    Normal test case.
    Multiple dots in acceptable poisitons in the domain and local part.

    Verifies that the email is updated successfully.
    """
    server_data = Server_data()

    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "multiple.dots.both.sides@valid.domain.edu.au"

    #Check whether the function call succeeds.
    assert user_profile_setemail(server_data, user_1_token, email) == {}

    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "multiple.dots.both.sides@valid.domain.edu.au"

#Attempts to assign an already-assigned email address to another account.
#This test should produce an error.
def test_email_already_taken():
    """
    Attempts to update a user's email to one that is already taken.

    InputError will occur.
    Verifies that user data is not updated.
    """
    server_data = Server_data()

    #Set token and email for first call
    user_1 = generate_user_1(server_data)
    user_1_token = user_1["token"]
    user_1_id = user_1["u_id"]

    email = "testemail@jrks1531testserver.com"

    #Check whether the call to user_profile_setemail succeeds.
    assert user_profile_setemail(server_data, user_1_token, email) == {}


    #Call the user function to check whether the details were updated correctly.
    updated_user = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user["user"]["email"] == "testemail@jrks1531testserver.com"

    #Set token for second call.
    #Email is the same as set before the first call.
    user_2 = generate_user_2(server_data)
    user_2_token = user_2["token"]
    user_2_id = user_2["u_id"]

    #Attempt to set email address with a different token
    #and the same email address.

    #InputError will occur as the email address is already in use
    #before the second call to user_profile_setemail.
    with pytest.raises(InputError):
        user_profile_setemail(server_data, user_1_token, email)

    #Verify that neither user (User 1 and 2) were not affected by the previous
    #attempt to set an already-in-use email to a different user.
    updated_user_1 = user_profile(server_data, user_1_token, user_1_id)
    assert updated_user_1["user"]["email"] == "testemail@jrks1531testserver.com"

    updated_user_2 = user_profile(server_data, user_2_token, user_2_id)
    assert updated_user_2["user"]["email"] == "patrick@test.com"
