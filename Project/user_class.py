# pylint: disable=C0301, W0105, R0902, R0913, R0904
'''
############## user_class.py ##################
A file for the user structures that will be used for the slackr backend server
It contains a class for user
Usage and description will be specified below
'''

'''
The user class stores permanent data on a particular user, and not store the temporary data such as the active token

***** Unique identifier - accessible: ******
Unique identifiers are used to access the function (private) elements

- u_id
- email
- password
- handle
- name_first
- name_last
- global_permission_id (This is the global permission)

To access unique identifer, please use your_object_name.unique_identifier
For example:

test_user.user_id = 1

***** Methods *****
Apart from the unique identifier, the following methods can be used:

+ is_owner_of_slackr() - return (boolean)
+ is_member_of_slackr() - return (boolean)

+ release_user_info - return {u_id, email, name_first, name_last, handle_str}

TODO can add more methods if needed

***** Debug use only ****
+ debug_printall() - print the content of the user

The user data structure is not handling password hashing, that should be done outside of the database as the database only stores, retrieve and modify data

The user is also not handling user_id generation - as it should be done by the server class

The user is also not handling handle generation - as it is a data set
'''

#import constants

class User:
    """
    User class
    a class that stores all user information in the backend server
    """

    # Used constructor
    # Registration should only happen with full inputs, here we assume the inputs have been checked outside of the object
    def __init__(self, u_id, email, hashed_password, name_first, name_last, handle, global_permission_id):
        """
        Constructor for the user class

        Input:
        - (int) u_id
        - (str) email
        - (str) hashed_password
        - (str) name_first
        - (str) name_last
        - (str) handle
        - (int) global_permission_id

        Output:
        - None
        """

        # Simply loading the data
        self._u_id = u_id
        self._email = email
        self._password = hashed_password
        self._handle = handle
        self._name_first = name_first
        self._name_last = name_last
        self._global_permission_id = global_permission_id
        self._channels_joined = []
        self._reset_code = ""
        self._profile_img_url = ""

    # Getter/Setter for user_id
    def get_u_id(self):
        """
        Getter function for u_id
        """
        return self._u_id

    def set_u_id(self, u_id):
        """
        Setter function for u_id
        """
        self._u_id = u_id

    # Getter/Setter for email
    def get_email(self):
        """
        Getter function for email
        """
        return self._email

    def set_email(self, email):
        """
        Setter function for email
        """
        self._email = email

    # Getter/Setter for password
    def get_password_hash(self):
        """
        Getter function for hashed password
        """
        return self._password

    def set_password_hash(self, password_hashed):
        """
        Setter function for hashed password
        """
        self._password = password_hashed

    # Getter/Setter for handle
    def get_handle(self):
        """
        Getter function for user handle
        """
        return self._handle

    def set_handle(self, handle):
        """
        Setter function for user handle
        """
        self._handle = handle

    # Getter/Setter for name_first
    def get_name_first(self):
        """
        Getter function for user first name
        """
        return self._name_first

    def set_name_first(self, name_first):
        """
        Setter function for user first name
        """
        self._name_first = name_first

    # Getter/Setter for name_last
    def get_name_last(self):
        """
        Getter function for user last name
        """
        return self._name_last

    def set_name_last(self, name_last):
        """
        Setter function for user last name
        """
        self._name_last = name_last

    # Getter/Setter for profile_img_url
    def get_profile_img_url(self):
        """
        Getter function for user profile image URL
        """
        return self._profile_img_url

    def set_profile_img_url(self, profile_img_url):
        """
        Setter function for user profile image URL
        """
        self._profile_img_url = profile_img_url

    # Getter/Setter for permission_global_id
    def get_global_permission_id(self):
        """
        Getter function for user global permission id
        """
        return self._global_permission_id

    def set_global_permission_id(self, global_permission_id):
        """
        Setter function for user global permission id
        """
        assert global_permission_id in (1, 2)
        self._global_permission_id = global_permission_id

    def get_reset_code(self):
        """
        Function to get reset code
        """
        return self._reset_code

    def set_reset_code(self, code):
        """
        Function to set the reset code
        """
        self._reset_code = code

    # Properties for public use
    u_id = property(get_u_id, set_u_id)
    email = property(get_email, set_email)
    password = property(get_password_hash, set_password_hash)
    handle = property(get_handle, set_handle)
    name_first = property(get_name_first, set_name_first)
    name_last = property(get_name_last, set_name_last)
    global_permission_id = property(get_global_permission_id, set_global_permission_id)
    reset_code = property(get_reset_code, set_reset_code)
    profile_img_url = property(get_profile_img_url, set_profile_img_url)

    # Methods
    # Release_user_info is used to create a dictionary that matches the agreed variable users, which contains u_id, email, name_first, name_last, handle_str, profile_img_url
    def release_user_info(self):
        """
        Function that packs user's information

        Output:
        - (dic) {u_id, email, name_first, name_last, handle_str, profile_img_url}
        """
        return {
            "u_id": self.u_id,
            "email": self.email,
            "name_first": self.name_first,
            "name_last": self.name_last,
            "handle_str": self.handle,
            "profile_img_url": self.profile_img_url,
        }

    # A shorter version of release user info, consist of {u_id, name_first, name_last}
    def get_user_member_info(self):
        """
        Function that packs user's information for channels

        Output:
        - (dic) {u_id, name_first, name_last, profile_img_url}
        """
        return {
            "u_id": self.u_id,
            "name_first": self.name_first,
            "name_last": self.name_last,
            "profile_img_url": self.profile_img_url
        }

    # Permission check, if the user is the owner of slackr (permission_id 1) return True, otherwise return False
    def is_owner_of_slackr(self):
        """
        Function that check if the user is an owner of slackr

        Output:
        - (bool) whether a user is an owner of slackr
        """
        if self._global_permission_id == 1:
            return True

        return False

    # if the user is the member of slackr (permission_id 2) return True, otherwise return False
    def is_member_of_slackr(self):
        """
        Function that checks if the user is a member of slackr

        Output:
        - (bool) whether a user is a member of slackr
        """
        if self._global_permission_id == 2:
            return True

        return False

    def does_reset_code_match(self, code):
        """
        Function to check if a reset code matches the code given

        Input:
        - (str) code
        Output:
        - (bool) whether if the code matches
        """
        if not self.reset_code:
            return False

        if self.reset_code == code:
            return True
        return False

    # for debugging only
    def debug_printall(self):
        """
        Function that debugs the user object
        """
        print("############### Debug print user object ###############")
        print(f"user_id: {self.u_id}")
        print(f"email: {self.email}")
        print(f"password: {self.password}")
        print(f"handle: {self.handle}")
        print(f"name_first: {self.name_first}")
        print(f"name_last: {self.name_last}")
        print(f"global_permission_id: {self.global_permission_id}")

'''
if __name__ == "__main__":
    newUser = user(20, "richard@gmail.com", "fkoij1f", "Richard", "Park", "richardpark", constants.PERMISSION_GLOBAL_OWNER)
    newUser.debug_printall()
    newUser.user_id = 1
    newUser.debug_printall()
'''
