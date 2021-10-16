# pylint: disable=C0301, R0902, R0904
'''
############## channel_class.py ##################
A file for the implementation of channels, that will be used in the backend server

The channel class stores permanent infomation of each individual on the server, it will contain all messages from the server, a list of owner's u_id and a list of member's u_id, and etc

the class will contain the following data:
- channel_id (unique)
- name
- list of message objects (latest first)
- list of owners (in u_id)
- list of members (in u_id)
- list of scheduled messages??

the class will contain the following methods:

** Constructor

** property / getter and setter
+ get_channel_id
+ set_channel_id
+ get_channel_name
+ set_channel_name

** message related:
+ get_message(message_id) - get message object with message_id
+ get_message_by_index(index) - get message object with index number
+ get_message_range(start, end) - get a list of message objects with the range specified
+ get_num_messages() - return the number of messages there are

+ create_message(message_id, u_id, message)? (TODO) create a message object and store it inside the channel, make sure the stored object is at front of the list as it is the most recent

+ create_message_later??

+ message_search(content) - a search function for a full match of the content supplied, return the list of message objects that matches the content

** Owner_list related:
+ get_owner_list - get the whole owner list
+ is_user_owner(u_id) - return True if the user is the LOCAL owner of the channel, False if not

+ channel_add_owner(u_id) - add a u_id into the owner list, no duplicates
+ channel_remove_owner(u_id) - remove this user from the owner list

** Member_list related:
+ get_member_list - get the whole member list
+ is_user_member(u_id) - return True if the user is the member of the channel, False if not
+ channel_add_member(u_id) - add a member to the channel, no duplicates
+ channel_removed_member(u_id) - remove a member from the channel

'''

from message_class import Message
from hangman_class import Hangman
import time_stamp as time

class Channel:
    """
    A class that handles channels data storages and its members/messages
    """

    # Constructors
    # The constructor takes in the channel_id, the name of the channel, and the info of the person created it
    def __init__(self, channel_id, name, created_by, is_public):
        """
        Used constructor - initializes all lists assign inputs

        Inputs:
            channel_id(int): the channel's unique ID
            name(string): the channel's name
            created_by(dic): the u_id of the creator of the channel

        Outputs:
            Nothing, initialization completes
        """
        self._channel_id = channel_id
        self._name = name
        self._is_public = is_public
        self._owner_list = []
        self._member_list = []
        self._message_list = []
        self._owner_list.append(created_by)
        self._member_list.append(created_by)

        # For standups:
        # Standup buffer is a list of strings
        self._standup_record = []
        self._time_finish = None
        self._is_standup_active = False
        self._standup_from = -1

        # For Hangman
        # Quit the app to make it inactive
        self._hangman_app = Hangman()

    # Methods
    # Getter/Setter - Properties
    def get_channel_id(self):
        """
        Getter function for _channel_id

        Outputs:
        - (int) - the channel id for this channel
        """
        return self._channel_id

    def set_channel_id(self, channel_id):
        """
        Setter function for _channel_id

        Inputs:
        - (int) the channel_id we want to set the channel to
        """
        self._channel_id = channel_id
        return True

    def get_channel_name(self):
        """
        Getter function for _name

        Output:
        - (str) the name of the channel
        """
        return self._name

    def set_channel_name(self, name):
        """
        Setter function for _name

        Inputs:
        - (str) the name we want to set the channel to
        """

        self._name = name
        return True

    def get_is_public(self):
        """
        Getter function for is_public variable

        Output:
        - (bool) whether if the channel is public
        """
        return self._is_public

    def set_is_public(self, is_public):
        """
        Setter function for is_public variable

        Input:
        - (bool) whether if the channel is public
        """
        self._is_public = is_public

    # Getter/setter for standup
    def get_time_finish(self):
        """
        Getter function for time_finish variable

        Output:
        - (int) the time_finish variable for standup
        """
        return self._time_finish

    def set_time_finish(self, time_finish):
        """
        Setter function for time_finish variable

        Input:
        - (int) the time_finish variable for standup
        """
        self._time_finish = time_finish

    def get_is_standup_active(self):
        """
        Getter function for is_standup_active variable

        Output:
        - (bool) whether a standup is currently active
        """
        return self._is_standup_active

    def set_is_standup_active(self, is_standup_active):
        """
        Setter function for is_standup_active variable

        Input:
        - (bool) whether a standup is currently active
        """
        self._is_standup_active = is_standup_active

    def get_hangman(self):
        """
        Getter function for hangman

        Output:
        - (obj) the hangman app
        """
        return self._hangman_app

    def set_hangman(self, hangman):
        """
        Setter function for hangman

        Input:
        Output:
        - (obj) the hangman app
        """
        self._hangman_app = hangman

    # Setting properties for easy usage
    channel_id = property(get_channel_id, set_channel_id)
    name = property(get_channel_name, set_channel_name)
    is_public = property(get_is_public, set_is_public)
    time_finish = property(get_time_finish, set_time_finish)
    is_standup_active = property(get_is_standup_active, set_is_standup_active)
    hangman = property(get_hangman, set_hangman)

    # Method for standup
    def get_standup_record(self):
        """
        Getter function for standup_record variable, consists of a list of standup messages they sent

        Output:
        - (array of str) Returning the standup records
        """
        return self._standup_record

    # Activating stand up takes in the length of the standup and return
    def activate_standup(self, length, u_id):
        """
        Activate_standup function
        A function to activate standup in the channel, assuming that all request that calls this function has been checked before (so it can not be called when there is already one active)

        Inputs:
        - (int) length: seconds to the end of standup
        - (int) u_id: user that started the standup
        Outputs:
        - (double) time_finish: timestamp
        """

        if not self.is_standup_active:
            timestamp = time.calculate_time_end(length)
            self.time_finish = timestamp
            self.is_standup_active = True
            self._standup_record = []
            self._standup_from = u_id
            return self.time_finish

        return None

    # Add a message to the standup record, append the handle before
    def add_standup_record(self, handle, message):
        """
        add_standup_record function
        A function to add a standup message to the active session. Assuming that the message inputs have been checked and they are valid

        Inputs:
        - (string) handle: handle of the person sending the message
        - (string) message: the message the person sent
        """
        msg = handle + ": " + message
        self._standup_record.append(msg)

    # when standup ends, combine the messages into one and send
    # if no one sent anything, print a message saying there has been no inputs
    def end_standup(self, message_id):
        """
        end_standup function
        A function to finish a standup message to the active session. only called by the server

        Inputs:
        - (int) the message ID that the final output will be assigned to
        """

        if len(self._standup_record) == 0:
            self._standup_record.append("Standup: No Message Recorded")

        message = "\n".join(self._standup_record)
        self.add_message(message_id, message, self._standup_from)

        # Clean up standups
        self.is_standup_active = False
        self._standup_record = []
        self._standup_from = None

    # Methods for owner_list
    # get_owner_list simply returns the list of owners of this channel in u_id
    def get_owner_list(self):
        """
        Getter function for _owner_list

        Output:
        - (list of dics) list of {u_ids, name_first, name_last, profile_img_url}
        """

        return self._owner_list

    # is_user_owner check if the user is an owner of the channel
    def is_user_owner(self, u_id):
        """
        Check if a user is the owner of the channel

        Input:
            u_id(int): the user's u_id

        Output:
            (bool) - whether the user is an owner of the channel
        """

        for owner in self._owner_list:
            if owner["u_id"] == u_id:
                return True

        return False

    # add_owner adds the user with u_id into the owner's list, and not do anything if the user is already an owner
    def add_owner(self, user_infos):
        """
        Add a user to the owner list for this channel

        Input:
        - user_infos {u_id, name_first, name_last}: the user's informations

        Output:
        - (bool) whether the operation succeeded - False if the user is already an owner of the channel
        """

        if self.is_user_owner(user_infos["u_id"]):
            return False

        self._owner_list.append(user_infos)
        self.add_member(user_infos)
        return True

    # remove_owner removes the user with u_id from the owner's list, and do nothing if the user does not exist in list
    def remove_owner(self, u_id):
        """
        Remove a user from the owner list for this channel

        Input:
        - u_id(int) the user's u_id

        Output:
        - (bool) whether the operation succeeded - False if the user does not exist in the list

        """
        if self.is_user_owner(u_id):
            self._owner_list = [owner for owner in self._owner_list if owner["u_id"] != u_id]
            return True

        return False

    # Methods for member's list
    # get_member_list simply returns the list of owners of this channel in u_id
    def get_member_list(self):
        """
        Retrieve a list of members from the channel

        Output:
        - (list of dics) - a list of the members of the channel

        """

        return self._member_list

    # is_user_member check if the user is an owner of the channel
    def is_user_member(self, u_id):
        """
        Check if a user is a member of the channel

        Inputs:
        - u_id(int) the search user id

        Outputs:
        - (bool) whether or not the user is a member of the channel

        """

        for member in self._member_list:
            if member["u_id"] == u_id:
                return True

        return False

    # add_member adds the user with u_id into the owner's list, and not do anything if the user is already an owner
    def add_member(self, user_infos):
        """
        Add a member to the channel

        Inputs:
        - user_infos {u_id, name_first, name_last}: the search user id

        Returns:
        - (bool) whether or not the operation is successful, False if the user is already a member of the channel

        """
        if self.is_user_member(user_infos["u_id"]):
            return False

        self._member_list.append(user_infos)
        return True

    # remove_member removes the user with u_id from the owner's list, and do nothing if the user does not exist in list
    def remove_member(self, u_id):
        """
        Remove a member from the channel

        Parameters:
        - u_id(int): the search user id

        Returns:
        - (bool) whether or not the operation is successful, False if the user is not a member of the channel

        """
        if self.is_user_member(u_id):
            self._member_list = [member for member in self._member_list if member["u_id"] != u_id]
            self.remove_owner(u_id)
            return True

        return False

    def get_num_members(self):
        """
        Getter function for number of members in channel

        Output:
        - (int) number of members
        """
        return len(self._member_list)

    def get_num_owners(self):
        """
        Getter function for number of owners in channel

        Output:
        - (int) number of owners
        """
        return len(self._owner_list)

    def get_num_messages(self):
        """
        Getter function for number of messages in channel

        Output:
        - (int) number of messages in the channel
        """
        return len(self._message_list)

    # Methods for messages:
    def get_message_list(self):
        """
        Get the entire list of the message object

        Output:
        - (list of obj) a list of message objects

        """

        return self._message_list

    # get_message obtain a message with message_id (unique) from the channel
    def get_message_by_id(self, message_id):

        """
        Get a message object with the message_id from the channel

        Parameters:
        - message_id(int): the unique identifier for messages

        Returns:
        - (obj) - a message object
        """

        # sudo code, might need to change
        message_list = self.get_message_list()
        for message in message_list:
            if message.message_id == message_id:
                return message

        return None

    # get_message_range get message objects by a certain index, not inclusive of the end index
    def get_message_range(self, start, end):
        """
        Get a range of messages indicated by the start and the end, not inclusive of the end

        Input:
        - start(int): the start of the message
        - end(int): the end of the message

        Output:
        - (obj) - a message object
        """
        if len(self._message_list) == 0:
            return []

        if len(self._message_list) < end or len(self._message_list) < start:
            return None

        if end == -1:
            sliced_message = self._message_list[start:]
        else:
            sliced_message = self._message_list[start:end]
        return sliced_message

    # does_message_exist checks if a message with message_id exists in the channel
    def does_message_exist(self, message_id):
        """
        Check if a message with message_id exists in the channel

        Inputs:
        - message_id(int) mesasge_id to search

        Outputs:
        - (bool) return if the message exists in the channel

        """
        for message in self._message_list:
            if message.message_id == message_id:
                return True

        return False

    # add_message adds a message into the channel, given its message_id (created by the server, message and who it is from (u_id))
    # The messages will be inserted to the front, instead of the back
    def add_message(self, message_id, message, u_id):
        """
        Create a new message for the channel and append it to the front, use time to get the current time

        Inputs:
        - message_id(int): mesasge_id to search

        Outputs:
        - (bool) return if the message exists in the channel

        """

        timestamp = time.get_timestamp_now()
        created_by = u_id

        new_message = Message(message_id, message, created_by, timestamp)

        self._message_list.insert(0, new_message)
        return True

    # Given a message_id, remove the message from the channel
    def remove_message(self, message_id):
        """
        Function to remove a message from the channel

        Inputs:
        - (int) message_id to be removed
        Outputs:
        - (bool) whether the operation is successful
        """

        if self.does_message_exist(message_id):
            self._message_list = [message for message in self._message_list if message.message_id != message_id]
            return True

        return False

    # The message_search function look for all message content in the channel to match the search_content, return a list of objects with a match
    def message_search(self, search_content):
        """
        Function to lookup a message from the channel

        Inputs:
        - (str) the search keyward
        Output:
        - (list of obj) message objects that matches this keyword
        """

        rt_obj = []
        for message_obj in self._message_list:
            if search_content in message_obj.message:
                rt_obj.append(message_obj)

        return rt_obj

    # Packing channel's info into a dictionary and return
    def pack_channel_details(self):
        """
        Function to package the channel's information

        Outputs:
        - (dic) {name, owner_members, all_members}
        """
        rt_details = {}
        rt_details["name"] = self.name
        rt_details["owner_members"] = self.get_owner_list()
        rt_details["all_members"] = self.get_member_list()

        return rt_details

    # Get channel info in format of {channel_id, name}
    def get_channel_infos(self):
        """
        Function to package basic info from the channel

        Outputs:
        - (dic) {channel_id, name}
        """
        return {
            "channel_id": self.channel_id,
            "name": self.name,
        }

    # Hangman related functions:
    def start_new_hangman_game(self):
        """
        A function to begin a new session of hangman game
        """
        self._hangman_app.reset()

    def is_hangman_game_active(self):
        """
        A function to check if a hangman game is currently active

        Output:
        - (bool) whether if a hangman game is active
        """
        return self._hangman_app.isactive()

if __name__ == "__main__":
    print("Testing usage of the channel_class")
