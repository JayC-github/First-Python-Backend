# pylint: disable=C0301, R0904
'''
############## message_class.py ##################
message_class is a sturcture for message objects that will be stored inside channels

the class will contain the following data:
- message_id (unique, across channels)
- message_content
- time_created
- created_by
- list of react objects
- is_pinned

the class will contain the following methods:

** Constructor
In the constructor when the message object is created, it must overload the default constructor and take in message_id, message, and initialize a default react with react_id 1, time stamp the current time of creation and set is_pinned to False

** Getter/Setter and Properties:
+ get_message_id()
+ set_message_id(message_id)
(Property)

+ get_message_content()
+ set_message_content(message_id)
(Property)

+ get_is_pinned()
+ set_is_pinned(is_pinned)
(Property)

+ get_time_created()
+ get_list_of_reacts()

** Reaction related methods
+ add_react_type(react_id) - create a new reaction with reaction_id
+ get_react(react_id) - get a react object with react_id
+ has_user_reacted(react_id, u_id) - return True if the user has reacted with this react_id, false if the user has not

** Other methods:
+ pack_message_info() - return a compatible structure specified in the spec - in this case {message_id, u_id, message, time_created, reacts, is_pinned}

'''

import constants as const
from reacts_class import Reacts

class Message:
    """
    Message class
    The class that handles message storage in a channel, it contains reacts and the message time and user ids
    """

    def __init__(self, message_id, message, created_by, time_stamp):

        """
        Used constructor:
        Initialize message_id, message, created_by, react list and a default react object called thumbs up

        Inputs:
        - message_id (int)
        - message (String)
        - created_by (int) u_id
        - time_stamp (int) timestamp coverted from date_time object

        Output:
        - None
        """
        self._message_id = message_id
        self._message = message
        self._created_by = created_by
        self._time_created = time_stamp
        self._reacts = []
        self._reacts.append(Reacts(const.REACT_THUMBS_UP_ID))
        self._is_pinned = False

    # Methods
    # Getter/Setters for message_id, message, created_by, time_stamp, is_pinned
    def get_message_id(self):
        """
        Getter function for message_id
        """
        return self._message_id

    def set_message_id(self, mesasge_id):
        """
        Setter function for message_id
        """
        self._message_id = mesasge_id

    def get_message(self):
        """
        Getter function for message
        """
        return self._message

    def set_message(self, message):
        """
        Setter function for message
        """
        self._message = message

    def get_creator(self):
        """
        Getter function for message creator
        """
        return self._created_by

    def set_creator(self, u_id):
        """
        Setter function for message creator
        """
        self._created_by = u_id

    def get_time_created(self):
        """
        Getter function for time created
        """
        return self._time_created

    def set_time_created(self, time_created):
        """
        Setter function for time created
        """
        self._time_created = time_created

    def get_is_pinned(self):
        """
        Getter function for is message pinned
        """
        return self._is_pinned

    def set_is_pinned(self, is_pinned):
        """
        Setter function for is message pinned
        """
        self._is_pinned = is_pinned

    # Set properties
    message_id = property(get_message_id, set_message_id)
    message = property(get_message, set_message)
    created_by = property(get_creator, set_creator)
    time_created = property(get_time_created, set_time_created)
    is_pinned = property(get_is_pinned, set_is_pinned)

    def get_list_of_reacts(self):
        """
        Getter function for the react list
        """
        return self._reacts

    # Reaction related methods
    def does_reaction_type_exist(self, react_id):
        """
        function that checks if a certain react exists in the message

        Input:
        - (int) react_id
        Output:
        - (bool) whether a react type with this id exists
        """
        for reaction in self._reacts:
            if reaction.react_id == react_id:
                return True

        return False

    def get_reacts_by_react_id(self, react_id):
        """
        function that gets the react list with the react_id

        Input:
        - (int) react_id
        Output:
        - (obj) the react object with the react_id
        """
        for reaction in self._reacts:
            if reaction.react_id == react_id:
                return reaction

        return None

    def add_new_react_type(self, react_id):
        """
        function that adds a new react type into the message

        Input:
        - (int) react_id to be created in the message
        """
        if not self.does_reaction_type_exist(react_id):
            self._reacts.append(Reacts(react_id))

    def add_new_reaction(self, react_id, u_id):
        """
        function that adds a new reaction to the message

        Input:
        - (int) react_id of the reaction
        - (int) u_id of the user making the reaction
        """
        react = self.get_reacts_by_react_id(react_id)
        react.add_user_reaction(u_id)

    def has_user_reacted(self, react_id, u_id):
        """
        function that checks if a user has reacted

        Input:
        - (int) react_id of the reaction
        - (int) u_id of the user making the reaction
        Output:
        - (bool) whether if the user has reacted
        """
        if self.does_reaction_type_exist(react_id):
            react = self.get_reacts_by_react_id(react_id)
            return react.does_u_id_exist_in_react(u_id)

        return False

    def remove_reaction(self, react_id, u_id):
        """
        function that removes a current reaction

        Input:
        - (int) react_id of the reaction
        - (int) u_id of the user making the reaction to be removed
        """
        if self.does_reaction_type_exist(react_id):
            react = self.get_reacts_by_react_id(react_id)
            if react.does_u_id_exist_in_react(u_id):
                react.remove_user_reaction(u_id)
                return True

        return False

    def react_clear(self, react_id):
        """
        function that empties a react type

        Input:
        - (int) react_id of the reaction to be cleared
        """
        if self.does_reaction_type_exist(react_id):
            react = self.get_reacts_by_react_id(react_id)
            react.clear_user_reactions()
            return True

        return False

    def remove_react_type(self, react_id):
        """
        function that removes a whole react type

        Input:
        - (int) react_id of the reaction to be removed
        """
        if self.does_reaction_type_exist(react_id):
            self._reacts = [react for react in self._reacts if react.react_id != react_id]
            return True

        return False

    def pack_all_reacts(self, u_id):
        """
        function that packs all reacts information base on the user

        Input:
        - (int) user ID of the user making such request
        """
        rt_reacts = []
        for react in self._reacts:
            rt_reacts.append(react.package_react_data(u_id))

        return rt_reacts

    def pack_message_info(self, u_id):
        """
        function that packs the whole message's information, including the reacts

        Input:
        - (int) user ID of the user making such request
        """
        rt_info = {}
        rt_info["message_id"] = self.message_id
        rt_info["u_id"] = self.created_by
        rt_info["message"] = self.message
        rt_info["time_created"] = self.time_created
        rt_info["reacts"] = self.pack_all_reacts(u_id)
        rt_info["is_pinned"] = self.is_pinned

        return rt_info

if __name__ == "__main__":
    pass
