#pylint: disable=R0801, C0301, W0212
'''
Quick pytest for user_class class, making sure that everything functions as expected
'''

import constants
from user_class import User

def test_properties():
    """
    Testing basic user properties
    """
    test_user = User(20, "richard@gmail.com", "fkoij1f", "Richard", "Park", "richardpark", constants.PERMISSION_GLOBAL_OWNER)

    # Test u_id getter
    assert test_user.u_id == 20

    # Test u_id setter
    test_user.u_id = 4
    assert test_user.u_id == 4

    # Test email getter
    assert test_user.email == "richard@gmail.com"
    # Test email setter
    test_user.email = "steven@gmail.com"
    assert test_user.email == "steven@gmail.com"

    # Test password getter
    assert test_user.password == "fkoij1f"
    # Test password setter
    test_user.password = "testpassword"
    assert test_user.password == "testpassword"

    # Test handle setter
    assert test_user.handle == "richardpark"
    # Test handle getter
    test_user.handle = "stevenyang"
    assert test_user.handle == "stevenyang"

    # Test name_first getter
    assert test_user.name_first == "Richard"
    # Test name_first setter
    test_user.name_first = "Steven"
    assert test_user.name_first == "Steven"
    assert test_user.name_first == test_user._name_first

    # Test name_last getter
    assert test_user.name_last == "Park"
    # Test name_last setter
    test_user.name_last = "Yang"
    assert test_user.name_last == "Yang"
    assert test_user.name_last == test_user._name_last

    # Test global_permission_id getter
    assert test_user.global_permission_id == constants.PERMISSION_GLOBAL_OWNER
    # Test global_permission_id setter
    test_user.global_permission_id = constants.PERMISSION_GLOBAL_MEMBER
    assert test_user.global_permission_id == constants.PERMISSION_GLOBAL_MEMBER

def test_methods():
    """
    Testing user methods
    """
    test_user = User(20, "richard@gmail.com", "fkoij1f", "Richard", "Park", "richardpark", constants.PERMISSION_GLOBAL_OWNER)

    assert test_user.is_owner_of_slackr()
    assert not test_user.is_member_of_slackr()

    assert test_user.release_user_info() == {
        "u_id": 20,
        "email": "richard@gmail.com",
        "name_first": "Richard",
        "name_last": "Park",
        "handle_str": "richardpark"
    }
