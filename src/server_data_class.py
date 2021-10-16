# pylint: disable=C0301, C0103, R0902, R0913, R0904
"""
############## server_data_class.py ##################
server_data class is the main class for the backend structures, it will use, store, record, modify objects inside and most functions should use this class for their operations

the class will contain the following data:
- a list of user objects
- a list of channel objects (which will have messages and reacts)
- a list of active sessions
(these three next variable are used to determine the id for the next object)
- next_u_id
- next_channel_id
- next_message_id

the class will contain the following methods:

** constructor:

** user related:
+ get_user(u_id) - get a user object with u_id, return None if not found
+ new_user(u_id, email, password_hashed, name_first, name_last, handle, global_permission_id)
+ remove_user()?? if needed?
+ does_email_exist(email)
+ does_user_exist(u_id)

** channel related:
+ get_channel(channel_id) - get a channel with channel_id (for any operations related to channels)
+ create_channel(channel_id, name, ... TODO) (for channel_create)
+ delete_channel(channel_id)

** session related
+ get_session_object

** Others TODO
+ server_debug_print()

** NEEN TO ADD
+ get_message_by_id directly

"""

from sessions_class import Sessions
from user_class import User
from channel_class import Channel

DEFAULT_U_ID_START = 5000000
DEFAULT_CHANNEL_ID_START = 0
DEFAULT_MESSAGE_ID_START = 0

class Server_data:
    """
    Server_data class
    a class that handles the backend data storage for the server
    """

    # server data initialization - doesn't need any input variables
    # Initialize the user object list and the channel object list
    def __init__(self):
        """
        Constructor for server_data class, initialize the internal variables
        """

        # Initialize the internal message object list
        self._user_list = []
        self._channel_list = []

        # Initialize the session object to handle sessions
        self._session_obj = Sessions()

        # Initialize the counter objects to 0
        self._next_u_id = DEFAULT_U_ID_START
        self._next_channel_id = DEFAULT_CHANNEL_ID_START
        self._next_message_id = DEFAULT_MESSAGE_ID_START

    # Methods
    # Getter/Setter for next_u_id
    def get_next_u_id(self):
        """
        Getter function for next_u_id
        """
        return self._next_u_id

    def set_next_u_id(self, u_id):
        """
        Setter function for next_u_id
        """
        self._next_u_id = u_id

    # Getter/Setter for next_channel_id
    def get_next_channel_id(self):
        """
        Getter function for next_channel_id
        """
        return self._next_channel_id

    def set_next_channel_id(self, channel_id):
        """
        Setter function for next_channel_id
        """
        self._next_channel_id = channel_id

    # Getter/Setter for next_message_id
    def get_next_message_id(self):
        """
        Getter function for next_message_id
        """
        return self._next_message_id

    def set_next_message_id(self, message_id):
        """
        Setter function for next_message_id
        """
        self._next_message_id = message_id

    # Getter for retrieveing sessions
    def get_sessions_list(self):
        """
        Getter function for session list
        """
        return self._session_obj

    # Getter for lists:
    def get_user_list(self):
        """
        Getter function for list of user objects
        """
        return self._user_list

    def get_channel_list(self):
        """
        Getter function for list of channel objects
        """
        return self._channel_list

    # Properties for getter and setter
    next_u_id = property(get_next_u_id, set_next_u_id)
    next_channel_id = property(get_next_channel_id, set_next_channel_id)
    next_message_id = property(get_next_message_id, set_next_message_id)

    # user related methods:
    # Check if a user exist given a u_id, return true if the user exists and false if it doesn't
    def num_users(self):
        """
        Function that returns number of users in the server

        Output:
        - (int) number of users in the server
        """
        return len(self._user_list)

    def does_user_exist(self, u_id):
        """
        Function that returns if a user with u_id exists

        Input:
        - (int) user_id to check
        Output:
        - (bool) whether if the user_id exists
        """
        for user in self._user_list:
            if user.u_id == u_id:
                return True

        return False

    # Find user by u_id in the user list, return the found object and raise exception if the user doesn't exist
    def get_user_by_id(self, u_id):
        """
        Function that gets the user object with the u_id

        Input:
        - (int) user_id to retrieve
        Output:
        - (obj) the user object from the user_id
        """
        for user in self._user_list:
            if user.u_id == u_id:
                return user

        return None

    # Since email is unique as well, we can check if an email exists in the list, with email passed in
    def does_email_exist(self, email):
        """
        Function that checks if the email already exists in the server

        Input:
        - (str) email to check
        Output:
        - (bool) whether the email exists in the server
        """
        for user in self._user_list:
            if user.email == email:
                return True

        return False

    def get_user_by_email(self, email):
        """
        Function that gets user object using their unique emails

        Input:
        - (str) email of a user
        Output:
        - (obj) the user object
        """
        for user in self._user_list:
            if user.email == email:
                return user

        return None

    def does_handle_exist(self, handle):
        """
        Function that checks if a handle already exists in the server

        Input:
        - (str) handle
        Output:
        - (bool) if the handle exists in the server
        """
        for user in self._user_list:
            if user.handle == handle:
                return True

        return False

    def does_reset_code_exist(self, code):
        """
        Function that checks if the reset code is valid

        Input:
        - (str) reset code
        Output:
        - (bool) whether if a reset code exists
        """
        for user in self._user_list:
            if user.reset_code == code:
                return True

        return False

    def get_user_by_reset_code(self, code):
        """
        A function that gets a user by a reset code,
        and returns none if not found

        Input:
        - (str) reset code
        Output:
        - (obj) get user by the reset code
        """
        for user in self._user_list:
            if user.reset_code == code:
                return user
        return None

    def remove_user(self, u_id):
        """
        A function that removes a user with the u_id from the server

        Input:
        - (int) u_id of the user to remove
        """
        self._user_list = [user for user in self._user_list if user.u_id != u_id]

    # Create a new user by using the following informations
    # u_id is provided by the next_u_id and will be returned from the function
    # move next_u_id up by 1 after successful registration
    # check if email is duplicate
    # return the u_id
    def new_user(self, email, hashed_password, name_first, name_last, handle, global_permission_id):
        """
        Function that adds a new user to the data storage

        Input:
        - (str) user's email
        - (str) user's hashed password
        - (str) user's first name
        - (str) user's last name
        - (str) user's handle
        - (str) user's global permission id
        Output:
        - (int) u_id of the user created
        """

        u_id = self.generate_u_id()
        user_new = User(u_id, email, hashed_password, name_first, name_last, handle, global_permission_id)
        self._user_list.append(user_new)

        return u_id

    # A function that clears all user objects in the list
    def user_list_clear(self):
        """
        Function that clears the user lists
        """
        self._user_list.clear()

    def pack_all_user_infos(self):
        """
        Function that packs a list of user informations from all users

        Output:
        - (array of dics) array of all user informations
        """
        rt_infos = []
        for user in self._user_list:
            rt_infos.append(user.release_user_info())

        return rt_infos

    # Check if a channel with channel_id exists in the server
    def does_channel_exist(self, channel_id):
        """
        Function that checks if a channel exists

        Input:
        - (int) channel_id
        Output:
        - (bool) whether if channel with channel_id exists
        """
        for channel in self._channel_list:
            if channel.channel_id == channel_id:
                return True

        return False

    # Retrieve a channel sepcified by the channel_id, raise exception if the channel is not found
    def get_channel_by_id(self, channel_id):
        """
        Function that gets a channel object by their channel_id

        Input:
        - (int) channel_id
        Output:
        - (obj) the channel object with channel_id
        """
        for channel in self._channel_list:
            if channel.channel_id == channel_id:
                return channel

        return None

    # Given the channel name and who is trying to create it, create a new channel with the information.
    # The channel_id is set by the server variable, and increase the variable by 1 after
    # created_by is a dic of the user info {u_id, name_first, name_last}
    # return the channel_id
    def num_channels(self):
        """
        Function that gets how many channels are in the server

        Output:
        - (int) number of channels in the server
        """
        return len(self._channel_list)

    def create_channel(self, channel_name, created_by, is_public):
        """
        Function that creates a channel in the server

        Input:
        - (str) channel_name
        - (int) u_id of the creator
        - (bool) whether if the channel is public
        Output:
        - (int) channel_id of the channel
        """
        channel_id = self.generate_channel_id()

        channel_obj = Channel(channel_id, channel_name, created_by, is_public)
        self._channel_list.append(channel_obj)

        return channel_id

    # Delete channel by ID, return false if the channel_id is not found
    def delete_channel(self, channel_id):
        """
        Function that deletes a channel off the server

        Input:
        - (int) channel_id to delete
        Output:
        - (bool) whether the operation is complete
        """
        if self.does_channel_exist(channel_id):
            self._channel_list = [channel for channel in self._channel_list if channel.channel_id != channel_id]
            return True

        return False

    def clear_channels(self):
        """
        Function that clears all channels in the server
        """
        self._channel_list.clear()

    # Pack all channel info, return a list of {channel_id, name}
    def pack_all_channel_infos(self):
        """
        Function that packs all channel informations to use

        Output:
        - (dic of arrays) {channels}
        """
        rt_infos = []
        for channel in self._channel_list:
            rt_infos.append(channel.get_channel_infos())

        return {"channels": rt_infos}

    def pack_channels_info_by_user(self, u_id):
        """
        Function that packs all channel information that a user is a member of

        Input:
        - (int) The user to pack infos
        Output:
        - (dic of arrays) {channels}
        """
        rt_infos = []
        for channel in self._channel_list:
            if channel.is_user_member(u_id):
                rt_infos.append(channel.get_channel_infos())

        return {"channels" : rt_infos}

    # Message functions - some functions doesnt have channel specified, so some message functions are necessary

    # Given a message_id, return the message_obj the id belongs to directly
    def find_message_by_message_id(self, message_id):
        """
        Function that finds a message object in the server by its message_id

        Input:
        - (int) message_id to look up
        Output:
        - (obj) the message object
        """
        for channel in self._channel_list:
            if channel.does_message_exist(message_id):
                return channel.get_message_by_id(message_id)

        return None

    # Give a message_id, return which channel it belongs to in channel_id
    def find_channel_by_message_id(self, message_id):
        """
        Function that finds a channel by a message inside

        Input:
        - (int) message_id to look up
        Output:
        - (int) the channel_id of the channel in which contains the message
        """
        for channel in self._channel_list:
            if channel.does_message_exist(message_id):
                return channel.channel_id

        return -1

    # Function to create a message_id for a message
    def generate_message_id(self):
        """
        Function that find the next valid usable message id in the server

        Output:
        - (int) next unique message_id
        """
        message_id = self.next_message_id
        self.next_message_id += 1

        return message_id

    def generate_u_id(self):
        """
        Function that finds the next valid user id to use

        Output:
        - (int) next unique u_id
        """
        u_id = self.next_u_id
        self.next_u_id += 1

        return u_id

    def generate_channel_id(self):
        """
        Function that find the next channel_id to use

        Output:
        - (int) next unique channel_id
        """
        channel_id = self.next_channel_id
        self.next_channel_id += 1

        return channel_id

    # RESET SERVER STATE
    def server_data_reset(self):
        """
        Function that resets the entire server
        """
        self._user_list.clear()
        self._channel_list.clear()
        self._session_obj.clear_all_sessions()

        self.next_u_id = DEFAULT_U_ID_START
        self.next_channel_id = DEFAULT_CHANNEL_ID_START
        self.next_message_id = DEFAULT_MESSAGE_ID_START
