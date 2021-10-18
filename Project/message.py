# pylint: disable=C0301, W0101, R1720
"""
################# message.py ####################
File for message related backend functions

Using resources from:
server_data_class
channel_class
session_class
message class
user_class
error

Contains functions:
message_send
message_remove
message_edit
message_react
message_unreact
message_pin
message_unpin
"""
#pylint: disable=line-too-long
#pylint: disable=trailing-whitespace
from error import AccessError, InputError

def message_send(server_data, token, channel_id, message):
    """
    message_send function:
    A function that sends a message to a given channel with channel_id

    Inputs:
    - server_data (obj)
    - token (string)
    - channel_id (int)
    - message (string)

    Outputs
    - {message_id} (dics)

    """
    hangman_cmd = "/hangman"
    guess_cmd = "/guess"
    if len(message) > 1000:
        raise InputError(description="Message is too long")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)

        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        channel_obj = server_data.get_channel_by_id(channel_id)

        # If use is an owner of slack just send the message
        if user_obj.is_owner_of_slackr() or channel_obj.is_user_member(u_id):
            message_id = server_data.generate_message_id()
            channel_obj.add_message(message_id, message, u_id)

            # check whether message is hangman and game is not active
            if message == "/hangman":         
                # set game to active and get hangman object
                channel_obj.start_new_hangman_game();
                hangman_obj = channel_obj.get_hangman()
                hangman_msg = "Hangman game started by {}!!!".format(user_obj.handle)  

                # add the message to the channel
                message_id_hangman = server_data.generate_message_id()
                channel_obj.add_message(message_id_hangman, hangman_msg, u_id)
            # else if check whether message is guess and game is already active
            elif message.startswith(guess_cmd) and channel_obj.is_hangman_game_active():

                hangman_obj = channel_obj.hangman
                # check if guess is a word or letter
                msg_str = message.split(" ")[1]
                print(f"msg_str is: {msg_str}")
                if len(msg_str) > 1:
                    # guess is a word
                    hangman_msg = hangman_obj.guess_word(msg_str)
                else: 
                    # guess is a letter
                    hangman_msg = hangman_obj.guess_letter(msg_str)

                # add the message to the channel
                message_id_hangman = server_data.generate_message_id()
                channel_obj.add_message(message_id_hangman, hangman_msg, u_id)
        else:
            # User is not a member of the channel
            raise AccessError(description="User is not authorised")
    else:
        raise AccessError(description="Invalid Token")

    return {"message_id": message_id}


def message_edit(server_data, token, message_id, message):
    """
    message_edit function:
    Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.

    Inputs:
    - server_data (obj)
    - token (string)
    - channel_id (int)
    - message (string)

    Outputs
    - {}

    """

    if len(message) > 1000:
        raise InputError(description="Message is too long")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)

        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        found_channel_id = server_data.find_channel_by_message_id(message_id)
        channel_obj = server_data.get_channel_by_id(found_channel_id)
        message_old = channel_obj.get_message_by_id(message_id)

        # User can only edit message if:
        # - User sent the message
        # - User is an owner of slack
        # - User is an owner of the channel where the message is in
        if message_old.created_by == u_id or user_obj.is_owner_of_slackr() or channel_obj.is_user_owner(u_id):
            # User is authorised so edit message content
            if not message == '':
                message_old.message = message
            else:
                channel_obj.remove_message(message_id)
        else:
            # User is not authorised
            raise AccessError(description="User is not authorised")
    else:
        raise AccessError(description="Invalid Token")

    return {}

def message_remove(server_data, token, message_id):
    """
    message_remove function:
    Given a message_id for a message, this message is removed from the channel

    Inputs:
    - server_data (obj)
    - token (string)
    - message (string)

    Outputs
    - {}

    """

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()

    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)

        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        found_channel_id = server_data.find_channel_by_message_id(message_id)
        channel_obj = server_data.get_channel_by_id(found_channel_id)

        if not found_channel_id == -1:
            # Message exists in a channel
            message_old = channel_obj.get_message_by_id(message_id)

            # User can only remove message if:
            # - User sent the message
            # - User is an owner of slack
            # - User is an owner of the channel where the message is in
            if message_old.created_by == u_id or  user_obj.is_owner_of_slackr() or channel_obj.is_user_owner(u_id):
                # User is authorised so remove message content
                channel_obj.remove_message(message_id)
            else:
                # User is not authorised
                raise AccessError(description="User is not authorised")
        else:
            # Message ID no longer exists
            raise InputError(description="Message does not exist")
    else:
        raise AccessError(description="Invalid Token")

    return {}

def message_react(server_data, token, message_id, react_id):
    """
    message_react function:
    Given a message within a channel the authorised user is part of, add a "react" to that particular message
    Inputs: 
    - server_data (obj)
    - token (string)
    - message_id (int)
    - react_id (int)
    
    Outputs
    - {}

    """
    # Frontend only has 1 react with id 1
    if react_id != 1:
        raise InputError(description="Not a valid react")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()
        
    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)

        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        found_channel_id = server_data.find_channel_by_message_id(message_id)
        channel_obj = server_data.get_channel_by_id(found_channel_id)

        if not found_channel_id == -1:
            # Message exists in a channel
            if channel_obj.is_user_member(u_id) or user_obj.is_owner_of_slackr():
                # User is a member of the channel or a slackr owner and can react
                message_obj = channel_obj.get_message_by_id(message_id)
                
                # Check if react ID exists
                if message_obj.does_reaction_type_exist(react_id) and (not message_obj.has_user_reacted(react_id, u_id)):
                    # React ID exists and user has not reacted
                    message_obj.add_new_reaction(react_id, u_id)
                else:
                    # React ID does not exist or user has already reacted
                    raise InputError(description="Invalid react") 
            else:
                # User cannot react
                raise InputError(description="User not authorised")
        else:
            raise InputError(description="Invalid message id") 
    else:
        raise AccessError(description="Invalid Token")

    return {}

def message_unreact(server_data, token, message_id, react_id):
    """
    message_unreact function:
    Given a message within a channel the authorised user is part of, remove a "react" to that particular message
    Inputs: 
    - server_data (obj)
    - token (string)
    - message_id (int)
    - react_id (int)
    
    Outputs
    - {}

InputError   
message_id is not a valid message within a channel that the authorised user has joined
react_id is not a valid React ID
Message with ID message_id does not contain an active React with ID react_id
    """
    # Frontend only has 1 react with id 1
    if react_id != 1:
        raise InputError(description="Not a valid react")

    # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()
        
    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)

        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        found_channel_id = server_data.find_channel_by_message_id(message_id)
        channel_obj = server_data.get_channel_by_id(found_channel_id)

        if not found_channel_id == -1:
            # Message exists in a channel
            if channel_obj.is_user_member(u_id) or user_obj.is_owner_of_slackr():
                # User is a member of the channel or a slackr owner and can react
                message_obj = channel_obj.get_message_by_id(message_id)
                
                # Check if react ID exists
                if message_obj.does_reaction_type_exist(react_id) and message_obj.has_user_reacted(react_id, u_id):
                    # React ID exists and user has reacted
                    message_obj.remove_reaction(react_id, u_id)
                else:
                    # React ID does not exist or user has not reacted
                    raise InputError(description="User has already reacted") 
            else:
                # User cannot react
                raise InputError(description="User not authorised")
        else:
            raise InputError(description="Invalid message id") 
    else:
        raise AccessError(description="Invalid Token")

    return {}

def message_pin(server_data, token, message_id):
    """
    message_pin function:
    Given a message within a channel, mark it as "pinned" to be given a special display treatment by the frontend

    Inputs: 
    - server_data (obj)
    - token (string)
    - message_id (int)
    
    Outputs
    - {}
    
    """

 # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()
        
    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)

        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        found_channel_id = server_data.find_channel_by_message_id(message_id)
        channel_obj = server_data.get_channel_by_id(found_channel_id)

        # Channel with message id exists
        if not found_channel_id == -1:
            if channel_obj.is_user_member(u_id):
                if channel_obj.is_user_owner(u_id) or user_obj.is_owner_of_slackr():
                    # User is a member of the channel or a slackr owner and can react
                    message_obj = channel_obj.get_message_by_id(message_id)
                    
                    # Check if already pinned
                    if not message_obj.get_is_pinned():
                        # Message is not pinned
                        message_obj.set_is_pinned(True)
                    else:
                        # Message is already pinned
                        raise InputError(description="Message already pinned") 
                else:
                    # User cannot react
                    raise InputError(description="User is an owner of the channel")
            else:
                raise AccessError(description="User is not a member of the channel")
        else:
            raise InputError(description="Not a valid message_id")
    else:
        raise AccessError(description="Invalid Token")

    return {}

def message_unpin(server_data, token, message_id):
    """
    message_unpin function:
    Given a message within a channel, mark it as "unpinned" to be given a special display treatment by the frontend

    Inputs: 
    - server_data (obj)
    - token (string)
    - message_id (int)
    
    Outputs
    - {}
    
    """

 # Obtain session object from server_data
    session_obj = server_data.get_sessions_list()
        
    # Check if the token is active
    if session_obj.is_token_active(token):
        # Get u_id from the active session
        u_id = session_obj.get_token_user(token)
        print(u_id)
        # Get user object and channel object
        user_obj = server_data.get_user_by_id(u_id)
        found_channel_id = server_data.find_channel_by_message_id(message_id)
        channel_obj = server_data.get_channel_by_id(found_channel_id)

        # Channel with message id exists
        if not found_channel_id == -1:
            if channel_obj.is_user_member(u_id):
                if channel_obj.is_user_owner(u_id) or user_obj.is_owner_of_slackr():
                    # User is a member of the channel or a slackr owner and can react
                    message_obj = channel_obj.get_message_by_id(message_id)
                    
                    # Check if already pinned
                    if not message_obj.get_is_pinned():
                        # Message is already unpinned
                        raise InputError(description="Message already pinned") 
                    else:
                        # Unpin message
                        message_obj.set_is_pinned(False)
                else:
                    # User cannot react
                    raise InputError(description="User is not an owner of the channel")
            else:
                raise AccessError(description="User is not a member of the channel")
        else:
            raise InputError(description="Not a valid message_id")
    else:
        raise AccessError(description="Invalid Token")

    return {}



if __name__ == "__main__":
    # Run some basic testing
    print("Compiled")
