# pylint: disable=C0301, W0105
#pylint: disable=R0801
'''
A file for helper functions written for test cases
'''

'''
Helper functions: Check if a channel exists in a list

channel_list is the variable "channels" returned from channel_list or channel_listall
'''

def does_channel_exist_in_list(channel_list, channel_id, name):
    """
    A function to check if a channel exists in a list of channels
    """
    for channel in channel_list:
        if (channel_id == channel["channel_id"] and name == channel["name"]):
            return True

    return False

def does_member_exist_in_list(member_list, u_id, name_first, name_last):
    """
    A function to check if a member exists in a list of members
    """
    for member in member_list:
        if (u_id == member["u_id"] and name_first == member["name_first"] and name_last == member["name_last"]):
            return True

    return False

# A function that generates number of strings as messages
def generate_messages(number):
    """
    A function to generate a number of messages and return them in the reverse order
    """
    count = 0
    list_of_msg = []
    while count < number:

        message_info = {}
        message_info["message"] = f"This is the {count} message"
        message_info["message_id"] = count
        list_of_msg.append(message_info)
        count += 1
    list_of_msg = list_of_msg[::-1]

    return list_of_msg

'''
if __name__ == "__main__":
    print (generate_messages(100))

'''
