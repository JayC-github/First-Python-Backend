# pylint: disable=C0301,W0105
"""
############## react_class.py ##################
a file for the implementation of the reactions, which will be used inside the message objects

Each of the react object represents a different type of react (thumb_up, thumb_down, etc) from the message, with their react_id only unique across the message (but not across the channels)

The class will contain the following data:

- react_id (referring to which id it is)
- list of u_id

The class will contain the following methods:
** constructor

** getter/setter property
+ get_react_id()
+ set_react_id(react_id)
(Property)

* Methods for u_id
+ does_u_id_exist_in_react(u_id) - return True if u_id exist in the list, False otherwise
+ add_u_id(u_id)
+ remove_u_id(u_id)
+ clear_u_id()
+ get_num_reactions()

* For others
+ package_react_data(u_id) - return information on the react object in the following format, the authroized user is u_id:
{react_id, u_ids, is_this_user_reacted}

"""

class Reacts:
    """
    React class
    a class for reactions of a message, stored inside message
    """

    def __init__(self, react_id):

        """
        Used constructor for the initialization

        Parameters:
            self: the object
            react_id(int): the type of reaction in ID

        Returns:
            nothing - should complete execution
        """

        self._react_id = react_id
        # Initialize the internal u_id list to be a list
        self._u_id_list = []

    # Methods
    # Getter/Setter for react_id
    def get_react_id(self):

        """
        Getter Method of _react_id

        Parameters:
            self: the object

        Returns:
            (int) - the_reaction_id of the object
        """

        return self._react_id

    def set_react_id(self, react_id):

        """
        Setter Method of _react_id

        Parameters:
            self: the object
            react_id(int): the reaction_id input

        Returns:
            (bool): whether or not the operation is complete
        """

        self._react_id = react_id
        return True

    # Property
    react_id = property(get_react_id, set_react_id)

    def get_user_reaction_list(self):

        """
        Getter Method of _u_id_list

        Parameters:
            self: the object

        Returns:
            (list of ints): a list of u_ids that has reacted
        """

        return self._u_id_list

    # Methods for u_id:
    def does_u_id_exist_in_react(self, u_id):

        """
        Check if a u_id exists in the reaction list

        Parameters:
            self: the object
            u_id(int): the target user_id for lookup

        Returns:
            (bool): whether if the u_id is found in the reaction
        """

        u_id_list = self.get_user_reaction_list()
        for u_id_temp in u_id_list:
            if u_id_temp == u_id:
                return True

        return False

    def add_user_reaction(self, u_id):

        """
        Adds a u_id into the reaction list

        Parameters:
            self: the object
            u_id(int): the target user_id for lookup

        Returns:
            (bool): whether if the adding operation is complete, false if the user already exists
        """

        if not self.does_u_id_exist_in_react(u_id):
            self._u_id_list.append(u_id)
            return True

        return False

    # Remove a u_id from the list, if the u_id exists
    def remove_user_reaction(self, u_id):

        """
        Removes a u_id from the reaction list

        Parameters:
            self: the object
            u_id(int): the target user_id for lookup

        Returns:
            (bool): whether if the removing operation is complete, false if the user is not found
        """

        if self.does_u_id_exist_in_react(u_id):
            self._u_id_list.remove(u_id)
            return True

        return False

    def get_num_reactions(self):

        """
        Get number of reactions from user

        Parameters:
            self: the object

        Returns:
            (int): number of reactions from users
        """

        return len(self._u_id_list)

    # Clear u_id list
    def clear_user_reactions(self):

        """
        Clear up all user reactions

        Parameters:
            self: the object

        Returns:
            (bool): whether or not the operation completes
        """
        self._u_id_list.clear()

    # package_react_data
    # return information on the react object in the following format, the authroized user is u_id: {react_id, u_ids, is_this_user_reacted}
    def package_react_data(self, u_id):

        """
        Package react data into complying standard for iteration

        Parameters:
            self: the object
            u_id(int): the user_id requesting such info

        Returns:
            (dic) - A dictionary containing keys:
                {"react_id"
                "u_ids"
                "is_this_user_reacted"}
        """

        is_this_user_reacted = self.does_u_id_exist_in_react(u_id)
        return {
            "react_id": self.react_id,
            "u_ids": self.get_user_reaction_list(),
            "is_this_user_reacted": is_this_user_reacted,
        }

'''
# Class usages:    
if __name__ == "__main__":

    # To create an object from the class, simply call:
    react_id = 0
    testReact = Reacts(react_id)

    # To obtain react_id, you can call the property react_id directly:
    react_id_from = testReact.react_id
    print(f"The react_id is: {react_id_from}")
    assert(react_id_from == 0)

    # To write value into react_id, call the property react_id directly
    testReact.react_id = 5
    assert(testReact.react_id == 5)
    print(f"The react_id after change is: {testReact.react_id}")

    # To call methods, use the objectName.functionName()
    # Adding a user to the reaction
    u_id = 5
    testReact.add_user_reaction(u_id)

    assert(testReact.get_num_reactions() == 1)
    print(f"There are currently {testReact.get_num_reactions()} users that has reacted")

    # Adding another user to the reaction
    u_id = 4
    testReact.add_user_reaction(u_id)
    assert(testReact.get_num_reactions() == 2)
    print(f"There are currently {testReact.get_num_reactions()} users that has reacted")

    # Adding another user to the reaction
    u_id = 2
    testReact.add_user_reaction(u_id)
    assert(testReact.get_num_reactions() == 3)
    print(f"There are currently {testReact.get_num_reactions()} users that has reacted")

    # Removing a user from the reaction
    u_id = 4
    testReact.remove_user_reaction(u_id)
    assert(testReact.get_num_reactions() == 2)
    print(f"There are currently {testReact.get_num_reactions()} users that has reacted after deletion")

    # Using the data package
    print(f"The react data package is: {testReact.package_react_data(2)}")

    # clear the user then use data package again
    testReact.clear_user_reactions()
    print(f"The react data package after clearing is: {testReact.package_react_data(2)}")
'''