# pylint: disable=C0301, W0105
'''
############## sessions_class.py ##################

A file for the implementation of the session object for the backend server, it is not a individual session but a class that holds active session records

All tokens inside the session_data are considered active, and all tokens that does not exist in the session_data are considered invalid/inactive

The class will contain the following data:
- session_data (a list of dictionary of {u_id, token})

# Methods
+ is_token_active(token) - given a token, check if it is in the list
+ get_token_user(token) - use the token to find out which user is holding the active token
+ get_user_tokens(u_id) - list a list of user's active tokens

+ create_active_session(u_id, token) - check if the token is duplicated, then create a session
+ end_active_session(token) - end a particular token's validity
+ end_user_session(u_id) - end a user's all sessions

+ clear_sessions() - clear all active sessions

'''

class Sessions:
    """
    Sessions class
    a class that records active sessions for the backend server
    """

    # Constructor
    # Default constructor - it initializes the list of session data
    def __init__(self):
        """
        constructor Sessions class
        simply initializes an empty array
        """
        self._session_data = []

    # Methods
    # Given a token, check if the token exists in the list
    def is_token_active(self, token):
        """
        Function that check if a token is active

        Input:
        - (str) token to check
        Output:
        - (bool) if the token is active
        """
        for session in self._session_data:
            temp_token = session[1]
            if temp_token == token:
                return True

        return False

    # Given a u_id, check if the user is active
    def is_user_active(self, u_id):
        """
        Function that check if a user is active

        Input:
        - (int) user_id to check
        Output:
        - (bool) if the u_id is active
        """
        for session in self._session_data:
            temp_user = session[0]
            if temp_user == u_id:
                return True

        return False

    # Given a token, retrieve which user the token belongs to and return its u_id, if the token is not valid, return -1
    def get_token_user(self, token):
        """
        Function that gets the user id of the input token

        Input:
        - (str) token
        Output:
        - (int) the u_id this token belongs to
        """
        for session in self._session_data:
            temp_user, temp_token = session
            if temp_token == token:
                return temp_user

        return -1

    # Given a u_id, return all tokens this user is currently holding
    def get_user_tokens(self, u_id):
        """
        Function that gets a user's all active tokens

        Input:
        - (int) u_id
        Output:
        - (list of str) list of tokens this user has
        """
        token_list = []
        for session in self._session_data:
            temp_user, temp_token = session
            if temp_user == u_id:
                token_list.append(temp_token)

        return token_list

    # The function returns the amount of active users right now
    def get_num_active_sessions(self):
        """
        Function that returns the number of active sessions on the server

        Output:
        - (int) number of sessions that are currently active
        """
        return len(self._session_data)

    # Given a u_id and a token, create an active session if the token is not a duplicate, return True if the session is active, False if there is an issue
    def create_active_session(self, u_id, token):
        """
        Function that creates an active session

        Input:
        - (int) u_id
        - (str) token
        Output:
        - (bool) whether if the token has been created
        """
        if not self.is_token_active(token):
            new_session = (u_id, token)
            self._session_data.append(new_session)
            return True

        return False

    # Given a token and end its session in the database, return True if successful and False if not
    def end_active_session(self, token):
        """
        Function that terminates an active sessions

        Input:
        - (str) token to end
        Output:
        - (bool) whether that session has been ended
        """
        if self.is_token_active(token):
            # Using list comprehension to remove a session
            self._session_data = [(temp_user, temp_token) for (temp_user, temp_token) in self._session_data if not temp_token == token]
            return True

        return False

    # Given a u_id and end all its sessions in the database, return True if successful and False if not
    def end_user_sessions(self, u_id):
        """
        Function that terminates a user's all active sessions

        Input:
        - (int) u_id for the user
        Output:
        - (bool) whether the operation is complete
        """
        if self.is_user_active(u_id):
            # Using list comprehension to remove a session
            self._session_data = [(temp_user, temp_token) for (temp_user, temp_token) in self._session_data if not temp_user == u_id]
            return True

        return False

    # Clear all current active sessions
    def clear_all_sessions(self):
        """
        Function that clears all active sessions
        """
        self._session_data.clear()
'''
    # A debugging function to print out how many sessions currently are actige
    def print_num_sessions(self):
        """
        Function that print debug values
        """
        print("######  Status report: Sessions  #####")
        print(f"There are currently {self.get_num_active_sessions()} sessions active")
'''

'''
if __name__ == "__main__":

    # Basic testing of the sessions
    test = sessions()

    token1 = "THISISAFAKETOKEN"
    u_id1 = 0

    print (test.is_user_active(0))
    print (test.is_token_active("Test Tokens"))

    test.create_active_session(u_id1, token1)
    print (test.is_user_active(u_id1))
    print (test.is_token_active("Test Tokens"))
    print (test.is_token_active(token1))

    print (f"The token belongs to user: {test.get_token_user(token1)}")

    token2 = "HAYDENSMITH"
    u_id2 = 5
    test.create_active_session(u_id2, token2)
    print (test.is_user_active(u_id2))
    print (test.is_token_active("Test Tokens"))
    print (test.is_token_active(token2))
    print (f"The token belongs to user: {test.get_token_user(token2)}")

    print (f"There are currently {test.get_num_active_sessions()} sessions active")

    test.end_user_sessions(u_id2)
    print (f"There are currently {test.get_num_active_sessions()} sessions active")

    test.clear_all_sessions()
    print (f"There are currently {test.get_num_active_sessions()} sessions active")

    test.print_num_sessions()

'''