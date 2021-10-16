"""
user.py
User functions module for Slackr
Robert Teoh for JRKS1531
This module contains user-related functions, for collecting user
profile data, and setting users' names, emails, and handles.

****IMPORT PIL!!!!****
****IMPORT URLLIB!!***

"""
import string
import random
import urllib
import PIL
import time

from PIL import Image

from error import AccessError, InputError

IMAGE_STORAGE_DIRECTORY = "images"
PROFILE_IMAGE_ACCESS_PATH = "/profile_image"


def user_profile(server_data, token, u_id):
    """
    Given a token and user_id, returns details about the user in a
    dictionary containing:
    u_id, email, name_first, name_last, handle_str

    Inputs:
    -server_data (Object)
    -token (String)
    -u_id (Integer)

    Outputs:
    -Dictionary in the format:
     {user:{user_data}}
     (only if call succeeds, i.e: error conditions not met)

    Error Conditions:
    -AccessError will occur if token is not valid.
    -InputError will occur if u_id given is not valid.
    """
    #Check that the token supplied is active.
    #If it is not then raise an AccessError.
    if token_status(server_data, token) != "TOKEN_ACTIVE":
        raise AccessError

    #Check that the user ID for the user of which we are querying the data exists.
    #If it does not then raise an InputError.
    user_exists = server_data.does_user_exist(u_id)
    if not user_exists:
        raise InputError

    user_obj = server_data.get_user_by_id(u_id)

    output = {}

    output["u_id"] = u_id
    output["email"] = user_obj.email
    output["name_first"] = user_obj.name_first
    output["name_last"] = user_obj.name_last
    output["handle_str"] = user_obj.handle
    output["profile_img_url"] = user_obj.profile_img_url

    return {"user": output}

#Return nothing
def user_profile_setname(server_data, token, name_first, name_last):
    """
    Given a token , first name and last name,
    updates the first and last name of the user with the specified token.

    Inputs:
    -server_data (Object)
    -token (String)
    -name_first (String)
    -name_last (String)

    Outputs:
    -{} (Empty dictionary) (If setname succeeded)

    Error conditions:
    -AccessError will occur if token is not valid.
    -InputError will occur if name_first or name_last given is not valid.
    """
    user_obj = {}

    #Check that the token supplied is active.
    #If it is not then raise an AccessError.
    if token_status(server_data, token) != "TOKEN_ACTIVE":
        raise AccessError

    #Check that the first and last names are within the length limits.
    #If either or both are not then raise InputError.
    name_length_within_limits = False

    if 1 <= len(name_first) <= 50 and 1 <= len(name_last) <= 50:
        name_length_within_limits = True

    if not name_length_within_limits:
        raise InputError

    #Set the user name
    user_obj = get_user(server_data, token)

    user_obj.name_first = name_first
    user_obj.name_last = name_last
    return {}

#Return nothing
def user_profile_setemail(server_data, token, email):
    """
    Given a token and email, updates the email of the user with the specified token.

    Inputs:
    -server_data (Object)
    -token (String)
    -email (String)

    Outputs:
    -{} (Empty dictionary) (If setemail succeeded)

    Error conditions:
    -AccessError will occur if token is not valid.
    -InputError will occur if the email given is not valid.
    -InputError will occur if the email given is already in use.
    """
    user_obj = {}

    #Check that the token supplied is active.
    #If it is not then raise an AccessError.
    if token_status(server_data, token) != "TOKEN_ACTIVE":
        raise AccessError

    #Check whether the email is valid.
    #If invalid then raise InputError.
    email_valid = is_email_valid(email)
    if not email_valid:
        raise InputError

    #Check whether the email is already taken.
    #If email taken then raise InputError.
    user_list = server_data.pack_all_user_infos()

    for user in user_list:
        if user["email"] == email:
            raise InputError

    #Set the email
    user_obj = get_user(server_data, token)

    user_obj.email = email

    return {}

#Return nothing
def user_profile_sethandle(server_data, token, handle_str):
    """
    Given a token and handle string (handle_str),
    updates the handle_str of the user with the specified token.

    Inputs:
    -server_data (Object)
    -token (String)
    -handle_str (String)

    Outputs:
    -{} (Empty dictionary) (If sethandle succeeded)

    Error conditions:
    -AccessError will occur if token is not valid.
    -InputError will occur if the handle_str given is not valid
    -InputError will occur if the handle_str given is already in use.
    """
    user_obj = {}

    #Check that the token supplied is active.
    #If it is not then raise an AccessError.
    if token_status(server_data, token) != "TOKEN_ACTIVE":
        raise AccessError

    #Check that the handle is within the length limits.
    #If it is not then raise InputError.
    handle_length_within_limits = False

    if 2 <= len(handle_str) <= 20:
        handle_length_within_limits = True

    if not handle_length_within_limits:
        raise InputError

    #Check whether the handle is already taken.
    #If handle taken then raise InputError.
    user_list = server_data.pack_all_user_infos()

    for user in user_list:
        if user["handle_str"] == handle_str:
            raise InputError

    #Set the handle
    user_obj = get_user(server_data, token)

    user_obj.handle = handle_str

    return {}

def users_all(server_data, token):
    """
    Given a token, returns all users' data.

    Inputs:
    -server_data (Object)
    -token (String)

    Outputs:
    -Dictionary in the format:
     {user:{users'_data}}
     (only if call succeeds, i.e: error conditions not met)

    Error conditions:
    -AccessError will occur if token is not valid.
    """

    #Check that the token supplied is active.
    #If it is not then raise an AccessError.
    if token_status(server_data, token) != "TOKEN_ACTIVE":
        raise AccessError

    output = server_data.pack_all_user_infos()

    return {"users": output}

def user_profile_uploadphoto(server_data, port, token, img_url, x_start, y_start, x_end, y_end):
    """
    Given a URL of an image on the internet and two coordinates:
    -crops the image within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
    -saves the cropped image to a local directory
    -generates a URL from which the image can be accessed by routes in server.py
    -adds the generated URL to the user's profile data

    Inputs:
    -server_data (Object)
    -port (Integer) (The port on which the backend server is running)
    -token (String)
    -img_url (String) (The URL from which we will grab the new profile image)
    -x_start (Integer)
    -y_start (Integer)
    -x_end (Integer)
    -y_end (Integer)

    Outputs:
    {} (empty dictionary)
     (only if call succeeds, i.e: error conditions not met)

    Error conditions:
    -AccessError will occur if token is not valid.
    -InputError will occcur if img_url returns HTTP status other than 200.
    -InputError will occur if any of x_start, y_start, x_end, y_end
     are not within the dimensions of the image at the source URL (img_url).
    -Image uploaded (image at img_url) is not a JPG
    """
    #Position (0,0) is the top left.

    #Check that the token supplied is active.
    #If it is not then raise an AccessError.
    if token_status(server_data, token) != "TOKEN_ACTIVE":
        raise AccessError

    user_obj = get_user(server_data, token)

    #Check the status code.
    status = urllib.request.urlopen(img_url).getcode()
    if status != 200:
        raise InputError('The image server returned an invalid status code (Not 200).')

    temp_filename, headers = urllib.request.urlretrieve(img_url)
    input_image_file = PIL.Image.open(temp_filename)
    input_image_width = input_image_file.width
    input_image_height = input_image_file.height

    #Check the file type of the image.
    #If the file type is not jpeg then raise InputError.
    file_type = headers.get_content_subtype()
    if file_type != 'jpeg' and file_type != 'jpg':
        raise InputError('The image provided is in an unsupported format. Please provide jpg images only.')

    #Generate the filename under which we will store the profile image.
    #The filename is the user's u_id.
    local_profile_image_filename = str(user_obj.u_id) + "-" + str(generate_random_string(10))

    #Save the image file to the profile_images folder/directory.
    local_profile_image_address = str(IMAGE_STORAGE_DIRECTORY) + '/profile_images/' + local_profile_image_filename

    #Check that the crop dimensions are within the image dimensions
    x_start = int(x_start)
    y_start = int(y_start)
    x_end = int(x_end)
    y_end = int(y_end)

    #Swap the start and end points such that start is in the top left, and end is in the bottom right.
    if x_start > x_end:
        temp = x_start
        x_start = x_end
        x_end = temp

    if y_start > y_end:
        temp = y_start
        y_start = y_end
        y_end = temp

    #If the crop dimensions are outside the dimensions of the image, raise InputError.
    if x_end > input_image_width or y_end > input_image_height:
        raise InputError("The area to be cropped is outside the image dimensions.")

    if x_start < 0 or y_start < 0:
        raise InputError("The area to be cropped is outside the image dimensions.")

    if x_end <= 0 or y_end <= 0:
        raise InputError("The area to be cropped is outside the image dimensions.")

    if x_start == x_end or y_start == y_end:
        raise InputError("The area to be cropped does not include any pixels. The start position must not be the same as the end position.")


    #Crop the image
    crop_points = (x_start, y_start, x_end, y_end)
    profile_image = input_image_file.crop(crop_points)

    #Save the cropped image to the local directory for processed images
    profile_image.save(local_profile_image_address + ".jpg", "JPEG")

    #Generate a link to the new profile image
    profile_img_url = "http://localhost:" + str(port) + str(PROFILE_IMAGE_ACCESS_PATH) + "/" + str(local_profile_image_filename) + ".jpg"

    #Set the profile image address
    user_obj = get_user(server_data, token)
    user_obj.profile_img_url = profile_img_url

    return {}


#Helper functions
def token_status(server_data, token):
    """
    Given a token, checks that the supplied token is active.
    Returns the token status.

    Inputs:
    -server_data (Object)
    -token (String)

    Outputs:
    -token_status (String)
     token status is either "TOKEN_ACTIVE" or "TOKEN_NOT_ACTIVE"
     corresponding to the status of the token.
    """
    sessions_list = server_data.get_sessions_list()

    if sessions_list.is_token_active(token):
        return "TOKEN_ACTIVE"

    return "TOKEN_NOT_ACTIVE"

def get_user(server_data, token):
    """
    Given a valid token, return the user object for the user that is
    authenticated with that token.

    Inputs:
    -server_data (Object)
    -token (String)

    Outputs:
    -get_user (Object)
     (The user object of the authenticated user.)
    """

    u_id = server_data.get_sessions_list().get_token_user(token)
    return server_data.get_user_by_id(u_id)

def is_email_valid(email):
    """
    Given an email address, checks that the email provided is a
    valid email address.

    Inputs:
    -email (String)

    Outputs:
    -is_email_valid (Boolean)
     is_email_valid returns True if the email address is valid,
     otherwise              False if them email address is not valid.
    """

    #Email address must contain 1 (and only 1) "@" character.
    if email.count("@") != 1:
        return False

    #Separate email address into local and domain parts.
    split_email = email.split("@")
    email_local = split_email[0]
    email_domain = split_email[1]

    #Email address must have a non-null local part and domain part.
    if not email_local:
        return False
    if not email_domain:
        return False

    #Local part must not start or end with '.'
    if email_local[0] == '.' or email_local[len(email_local) - 1] == '.':
        return False

    #'..' must not be anywhere in the local part
    if ".." in email_local:
        return False

    #Check that all the characters in the local part are valid.
    for char in email_local:
        valid_char = False
        if char in "!#$%&'*+-/=?^_`{|}~":
            valid_char = True
        if char in string.ascii_lowercase or char in string.ascii_uppercase or char in "1234567890.":
            valid_char = True
        if not valid_char:
            return False

    #The last character of the local and domain parts must not be '-'.
    if email_local[len(email_local) - 1] == '-' or email_domain[len(email_domain) - 1] == '-':
        return False

    #Domain must contain '.'
    if not "." in email_domain:
        return False

    #'..' must not be anywhere in the domain
    if ".." in email_domain:
        return False

    #Domain must not start or end with '.' or '-'
    if email_domain[0] == '-' or email_domain[len(email_domain) - 1] == '-':
        return False
    if email_domain[0] == '.' or email_domain[len(email_domain) - 1] == '.':
        return False

    #Check that all the characters in the domain are valid.
    for char in email_domain:
        valid_char = False
        if char in string.ascii_lowercase or char in string.ascii_uppercase or char in "1234567890.":
            valid_char = True
        if char == '-':
            valid_char = True
        if not valid_char:
            return False

    #If email is valid return True (otherwise we will not reach the line below).
    return True

def generate_random_string(desired_length):
    """
    Generates a random string and appends the system timestamp onto the end of it.

    Inputs:
    -desired_length (Integer)

    Outputs:
    -output_string (String)
    """
    valid_chars = string.ascii_uppercase + string.digits

    string_length = 0
    output_string = ""

    while string_length < desired_length:
        output_string += str(random.choice(valid_chars))
        string_length += 1

    output_string += str(int(time.time()))

    return str(output_string)
