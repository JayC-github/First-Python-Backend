# pylint: disable=C0301, W0603, C0103, C0302
"""
################ server.py ###################
The main file for the backend server, contains all the routes and the multithreaded handling of certain functions

"""

import sys
import threading
import time
from json import dumps
from flask import Flask, request, send_file
from flask_cors import CORS

import data_storage
from error import InputError
from time_stamp import get_timestamp_now
from server_data_class import Server_data
from auth import auth_register, auth_login, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from channel import channel_invite, channel_details, channel_messages, channel_join, channel_leave, channel_addowner, channel_removeowner
from channels import channels_create, channels_list, channels_listall
from message import message_send, message_edit, message_remove, message_react, message_unreact, message_pin, message_unpin
from message_schedule import process_message_infos, send_delayed_message
from search import search
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile_uploadphoto, users_all
from admin import admin_userpermission_change
from standup import standup_start, standup_send, standup_active, end_standup
from input_handling import input_handle_ids
from remove_user import remove_user

def defaultHandler(err):
    """
    Error handler
    """
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

def create_server_data_obj():
    """
    a function to create a server_data object for this active server

    Input:
    - None
    Output:
    - (obj) a server_data object either read from file or create as new
    """
    if data_storage.does_file_exist():
        print("Found local storage, loading the server state...")
        return data_storage.load_state()

    print("No local storage found, creating a default server state...")
    return Server_data()

# Gobal data storage:
SERVER_DATA = create_server_data_obj()

PROFILE_IMAGE_DIRECTORY = "images/profile_images"

def get_server_data_obj():
    """
    A function to return the server object stored globally

    Input:
    - None
    Output:
    - (obj) a server_data object used by the server
    """
    global SERVER_DATA
    server = SERVER_DATA
    return server

# An exit signal for save data
EXIT_SIGNAL = False

def get_signal():
    """
    A function to return the global signal for use

    Input:
    - None
    Output:
    - (bool) a exit signal to use by other functions
    """
    global EXIT_SIGNAL
    return EXIT_SIGNAL

def exit_signal_received():
    """
    A function to change the global exit signal as the exit signal is received

    Input:
    - None
    Output:
    - None
    """
    global EXIT_SIGNAL
    EXIT_SIGNAL = True

def save_data_period(time_in_seconds):
    """
    A multi threaded function to save data every seconds specified in the input

    Input:
    - (int) time_in_seconds
    Output:
    - None
    """
    while not get_signal():
        time.sleep(time_in_seconds)
        data_storage.save_state(get_server_data_obj())
    print("End data saved, exiting...")

MESSAGE_QUEUE = []

def get_message_queue():
    """
    A function to retrieve the global message queue, thats built for message send later

    Input:
    - None
    Output:
    - (array) an array of messages
    """
    global MESSAGE_QUEUE
    return MESSAGE_QUEUE

def set_message_queue(new_queue):
    """
    A method to update the global message queue

    Input:
    - (array) an array of messages
    Output:
    - None
    """
    global MESSAGE_QUEUE
    MESSAGE_QUEUE = new_queue

def message_sendlater_handler():
    """
    A multithreaded handler for sending message late, it checks the time every second and send out messages in the queue if they reached their scheduled time

    Input:
    - None
    Output:
    - None
    """
    while not get_signal():
        message_id_done = []

        message_queue_in = get_message_queue()
        time.sleep(2)

        if len(message_queue_in) > 0:

            time_now = get_timestamp_now()
            for message_to_send in message_queue_in:
                if message_to_send["time_sent"] <= time_now:

                    print(f"Sending scheduled message: {message_to_send}")
                    server_data = get_server_data_obj()
                    # Send the message and delete it from the queue
                    send_delayed_message(server_data, message_to_send)

                    # Append the message_id to the done list
                    message_id_done.append(message_to_send["message_id"])

            message_queue_in = [message for message in message_queue_in if message["message_id"] not in message_id_done]
            set_message_queue(message_queue_in)

    print("Terminating Scheduled messages... the messages that are still in the queue will be lost")

def standup_handler(channel_id, time_finish):
    """
    A multithreaded handler for dealing with standups in a specific channel

    Input:
    - (int) channel_id
    - (int) time_finish: a UTC timestamp
    Output:
    - None
    """
    while get_timestamp_now() < time_finish:
        print(get_timestamp_now())
        time.sleep(1)

    # time's up here, get server_data and get channel before calling the end of standup
    print("time's up! ending standup")
    server_data = get_server_data_obj()
    end_standup(server_data, channel_id)

def update_profile_image_address_port(port):
    """
    Given the port on which the server is to run, updates all users' profile_img_url to reflect any change in the port.
    If the port did not change then the users' profile_img_url will not be modified.

    Input:
    - port (Integer)
    Output:
    - {} (empty dictionary)
    """
    server_data = get_server_data_obj()
    users = server_data.pack_all_user_infos()
    if not users:
        return {}
    port_string = ":" + str(port)
    port_replacement_needed = False
    for user in users:
        sample_profile_img_url = user["profile_img_url"]
        if sample_profile_img_url:
            if port_string in sample_profile_img_url:
                port_replacement_needed = False
            else:
                port_replacement_needed = True
                previous_port = sample_profile_img_url.split(":")[2]
                previous_port = previous_port.split("/")[0]

    if port_replacement_needed:
        #Get list of user IDs to update (u_id)
        u_id_list = []
        for user in users:
            if user["profile_img_url"]:
                u_id_list.append(user["u_id"])

        #Update all users' image link.
        for u_id in u_id_list:
            user_obj = server_data.get_user_by_id(u_id)
            replacement_profile_img_url = user_obj.profile_img_url.replace(":" + str(previous_port), port_string)
            user_obj.profile_img_url = replacement_profile_img_url

    return {}

# HTTP Routes
@APP.route("/auth/login", methods=['POST'])
def http_auth_login():
    """
    http_auth_login:
    Given a registered user's email and password in JSON data, generates a valid token for the user to remain authenticated and convert it into JSON data for transmission

    Input:
    - (JSON) {email, password}
    output:
    - (JSON) {u_id, token}
    """
    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    # Call the processing function and expect raw data output
    output_data = auth_login(server_data, input_data["email"], input_data["password"])

    return dumps(output_data)

@APP.route("/auth/logout", methods=['POST'])
def http_auth_logout():
    """
    http_auth_logout:
    Given a token, if it's active, invalidates the token to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false

    Input:
    - (JSON) {token}
    Output:
    - (JSON) {is_success}
    """
    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    # Call the processing function and expect raw data output
    output_data = auth_logout(server_data, input_data["token"])
    return dumps(output_data)

@APP.route("/auth/register", methods=['POST'])
def http_auth_register():
    """
    http_auth_register:
    Given a user's first and last name, emaill address, and password, create a new account for them and return a token for authentication in their session.

    Input:
    - (JSON) {email, password, name_first, name_last}
    Output:
    - (JSON) {u_id, token}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = auth_register(server_data, input_data["email"], input_data["password"], input_data["name_first"], input_data["name_last"])
    return dumps(output_data)

@APP.route("/auth/passwordreset/request", methods=['POST'])
def http_auth_passwordreset_request():
    """
    http_auth_passwordreset_request
    Given a user's email address, create a secret code for reseting the
    password and send to his/her email address.

    Input:
    - (JSON) {email}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = auth_passwordreset_request(server_data, input_data["email"])
    return dumps(output_data)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def http_auth_passwordreset_reset():
    """
    http_auth_passwordreset_request
    Given a user's email address, create a secret code for reseting the
    password and send to his/her email address.

    Input:
    - (JSON) {reset_code, new_password}
    Output:
    - (JSON) {}
    """
    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = auth_passwordreset_reset(server_data, input_data["reset_code"], input_data["new_password"])
    return dumps(output_data)

@APP.route("/channel/invite", methods=['POST'])
def http_channel_invite():
    """
    http_channel_invite:
    Invites a user to join a channel with channel_id. Once invited the user is added to the channel immediately

    Input:
    - (JSON) {token, channel_id, u_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    channel_id = -1
    u_id = -1

    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])
    u_id = input_handle_ids(input_data["u_id"])

    output_data = channel_invite(server_data, input_data["token"], channel_id, u_id)
    return dumps(output_data)

@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    """
    http_channel_details:
    Given a channel with channel_id that the authorized user is a part of, provide basic details about the channel

    Input:
    - (URL) {token, channel_id}
    Output:
    - (JSON) {name, owner_members, all_members}
    """

    # Get input and server data
    input_token = request.args.get("token")
    input_channel_id = input_handle_ids(request.args.get("channel_id"))
    server_data = get_server_data_obj()

    output_data = channel_details(server_data, input_token, input_channel_id)

    return dumps(output_data)

@APP.route("/channel/messages", methods=['GET'])
def http_channel_messages():
    """
    http_channel_messages:
    Given a channel with channel_id that the user is a part of, return up to 50 messages between index start and start+50 exclusive. 0 is the most recent message

    Input:
    - (URL) {token, channel_id, start}
    Output:
    - (JSON) {message, start, end}
    """

    # Get input and server data
    input_token = request.args.get("token")
    input_channel_id = input_handle_ids(request.args.get("channel_id"))
    input_start = input_handle_ids(request.args.get("start"))
    server_data = get_server_data_obj()

    output_data = channel_messages(server_data, input_token, input_channel_id, input_start)
    return dumps(output_data)

@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    """
    http_channel_leave:
    Gievn a channel ID, the user removed as a member of this channel

    Input:
    - (JSON) {token, channel_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])

    output_data = channel_leave(server_data, input_data["token"], channel_id)
    return dumps(output_data)

@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    """
    http_channel_join:
    Given a channel_id of a channel that the authorized user can join, adds them to that channel

    Input:
    - (JSON) {token, channel_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])

    output_data = channel_join(server_data, input_data["token"], channel_id)
    return dumps(output_data)

@APP.route("/channel/addowner", methods=['POST'])
def http_channel_addowner():
    """
    http_channel_addowner:
    Make user with user id u_id an owner of this channel

    Input:
    - (JSON) {token, channel_id, u_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])
    u_id = input_handle_ids(input_data["u_id"])

    output_data = channel_addowner(server_data, input_data["token"], channel_id, u_id)
    return dumps(output_data)

@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_removeowner():
    """
    http_channel_removeowner:
    Remove user with u_id an owner of this channel

    Input:
    - (JSON) {token, channel_id, u_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])
    u_id = input_handle_ids(input_data["u_id"])

    output_data = channel_removeowner(server_data, input_data["token"], channel_id, u_id)
    return dumps(output_data)

@APP.route("/channels/list", methods=['GET'])
def http_channels_list():
    """
    http_channels_list:
    Provide a list of all channels that the authorized user is a part of

    Input:
    - (URL) {token}
    Output:
    - (JSON) {channels}
    """

    # Get input and server data
    input_data = request.args.get("token")
    server_data = get_server_data_obj()

    output_data = channels_list(server_data, input_data)
    return dumps(output_data)

@APP.route("/channels/listall", methods=['GET'])
def http_channels_listall():
    """
    http_channels_listall:
    Provide a list of all channels

    Input:
    - (URL) {token}
    Output:
    - (JSON) {channels}
    """

    # Get input and server data
    input_data = request.args.get("token")
    server_data = get_server_data_obj()

    output_data = channels_listall(server_data, input_data)
    return dumps(output_data)

@APP.route("/channels/create", methods=['POST'])
def http_channels_create():
    """
    http_channels_create:
    Creates a new channel with that name that is either a public or private channel

    Input:
    - (JSON) {token, name, is_public}
    Output:
    - (JSON) {channel_id}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = channels_create(server_data, input_data["token"], input_data["name"], input_data["is_public"])
    return dumps(output_data)

@APP.route("/message/send", methods=['POST'])
def http_message_send():
    """
    http_message_send:
    Send a message from authorised_user to the channel specified by channel_id

    Input:
    - (JSON) {token, channel_id, message}
    Output:
    - (JSON) {message_id}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])

    output_data = message_send(server_data, input_data["token"], channel_id, input_data["message"])
    return dumps(output_data)

@APP.route("/message/sendlater", methods=['POST'])
def http_message_sendlater():
    """
    http_message_sendlater:
    Send a message from authorized_user to the channel specified by channel_id automatically at a secified time in the future

    Input:
    - (JSON) {token, channel_id, message, time_sent}
    Output:
    - (JSON) {message_id}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])

    # Construct the necessary information here
    message_info = process_message_infos(server_data, input_data["token"], channel_id, input_data["message"], int(input_data["time_sent"]))

    queue = get_message_queue()
    queue.append(message_info)

    return dumps({
        "message_id": message_info["message_id"]
    })

@APP.route("/message/react", methods=['POST'])
def http_message_react():
    """
    http_message_react:
    Given a message within a channel the authorized user is a part of, add a "react to that particular message

    Input:
    - (JSON) {token, message_id, react_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    message_id = input_handle_ids(input_data["message_id"])
    react_id = input_handle_ids(input_data["react_id"])

    output_data = message_react(server_data, input_data["token"], message_id, react_id)
    return dumps(output_data)

@APP.route("/message/unreact", methods=['POST'])
def http_message_unreact():
    """
    http_message_unreact:
    Given a message within a channel the authorized user is a part of, remove a react to that particular message

    Input:
    - (JSON) {token, message_id, react_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    message_id = input_handle_ids(input_data["message_id"])
    react_id = input_handle_ids(input_data["react_id"])

    output_data = message_unreact(server_data, input_data["token"], message_id, react_id)
    return dumps(output_data)

@APP.route("/message/pin", methods=['POST'])
def http_message_pin():
    """
    http_message_pin:
    Given a message within a channel, mark it as pinned to be given special display treatment by the front end

    Input:
    - (JSON) {token, message_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    message_id = input_handle_ids(input_data["message_id"])

    output_data = message_pin(server_data, input_data["token"], message_id)
    return dumps(output_data)

@APP.route("/message/unpin", methods=['POST'])
def http_message_unpin():
    """
    http_message_unpin:
    Given a message within a channel, mark it as unpinned

    Input:
    - (JSON) {token, message_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    message_id = input_handle_ids(input_data["message_id"])

    output_data = message_unpin(server_data, input_data["token"], message_id)
    return dumps(output_data)

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    """
    http_message_remove:
    Given a message_id for a message, this message is removed from the channel

    Input:
    - (JSON) {token, message_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    message_id = input_handle_ids(input_data["message_id"])

    output_data = message_remove(server_data, input_data["token"], message_id)
    return dumps(output_data)

@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    """
    http_message_edit:
    Given a message, update it's text with new text. If new message is an empty string, the message is deleted.

    Input:
    - (JSON) {token, message_id, message}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    message_id = input_handle_ids(input_data["message_id"])

    if not input_data["message"]:
        output_data = message_remove(server_data, input_data["token"], message_id)
    else:
        output_data = message_edit(server_data, input_data["token"], message_id, input_data["message"])

    return dumps(output_data)

@APP.route("/user/profile", methods=['GET'])
def http_user_profile():
    """
    http_user_profile:
    For a valid user, returns information about their user_id, email, first name, last name and handle

    Input:
    - (URL) {token, u_id}
    Output:
    - (JSON) {user}
    """

    # Get input and server data

    input_token = request.args.get("token")
    input_u_id = input_handle_ids(request.args.get("u_id"))
    server_data = get_server_data_obj()

    output_data = user_profile(server_data, input_token, input_u_id)
    return dumps(output_data)

@APP.route("/user/profile/setname", methods=['PUT'])
def http_user_profile_setname():
    """
    http_user_profile_setname:
    Update the authorized user's first and last name

    Input:
    - (JSON) {token, name_first, name_last}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = user_profile_setname(server_data, input_data["token"], input_data["name_first"], input_data["name_last"])
    return dumps(output_data)

@APP.route("/user/profile/setemail", methods=['PUT'])
def http_user_profile_setemail():
    """
    http_user_profile_setemail:
    Update the authorized user's email

    Input:
    - (JSON) {token, email}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = user_profile_setemail(server_data, input_data["token"], input_data["email"])
    return dumps(output_data)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def http_user_profile_sethandle():
    """
    http_user_profile_sethandle:
    Update the authorized user's handle/display name

    Input:
    - (JSON) {token, handle_str}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    output_data = user_profile_sethandle(server_data, input_data["token"], input_data["handle_str"])
    return dumps(output_data)

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def http_user_profile_uploadphoto():
    """
    http_user_profile_uploadphoto:
    Update the authorized user's profile photo link

    Input:
    - (JSON) {token, img_url, x_start, y_start, x_end, y_end}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()

    #Get port as variable
    port = (int(sys.argv[1]) if len(sys.argv) == 2 else 8080)

    output_data = user_profile_uploadphoto(server_data, port, input_data["token"], input_data["img_url"], input_data["x_start"], input_data["y_start"], input_data["x_end"], input_data["y_end"])
    return dumps(output_data)

@APP.route("/profile_image/<string:filename>")
def http_user_profile_image(filename):
    """
    http_imgurl:
    """
    file_address = str(PROFILE_IMAGE_DIRECTORY) + "/" + str(filename)

    return send_file(file_address, mimetype='image/jpeg')

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    """
    http_users_all:
    Returns a list of all users and their associated details

    Input:
    - (URL) {token}
    Output:
    - (JSON) {users}
    """

    # Get input and server data
    input_data = request.args.get("token")
    server_data = get_server_data_obj()

    output_data = users_all(server_data, input_data)

    return dumps(output_data)

@APP.route("/search", methods=['GET'])
def http_search():
    """
    http_search:
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query. Results are sorted from most recent message to least recent message

    Input:
    - (URL) {token, query_str}
    Output:
    - (JSON) {messages}
    """

    # Get input and server data
    input_token = request.args.get("token")
    input_query_str = request.args.get("query_str")
    server_data = get_server_data_obj()

    output_data = search(server_data, input_token, input_query_str)
    return dumps(output_data)

@APP.route("/standup/start", methods=['POST'])
def http_standup_start():
    """
    http_standup_start:
    For a given channel, start the stand up period whereby for the next "length" seconds if someone calls "standup_send" with a message, it is buffered during the X second window then at the end of the X second window a message will be added to the message queue in the channel from the user who started the standup. X is an integer that denotes the number of seconds that the standup occurs for

    Input:
    - (JSON) {token, channel_id, length}
    Output:
    - (JSON) {time_finish}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])
    length = input_handle_ids(input_data["length"])
    output = standup_start(server_data, input_data["token"], channel_id, length)

    #create a multithread on the standup
    thread = threading.Thread(target=standup_handler, args=(channel_id, int(output["time_finish"])))
    thread.start()

    return dumps(output)

@APP.route("/standup/active", methods=['GET'])
def http_standup_active():
    """
    http_standup_active:
    For a given channel, return whether a standup is active in it, and what time the standup finishes. If no standup is active then time_finish returns None

    Input:
    - (URL) {token, channel_id}
    Output:
    - (JSON) {is_active, time_finish}
    """

    # Get input and server data
    input_token = request.args.get("token")
    input_channel_id = input_handle_ids(request.args.get("channel_id"))
    server_data = get_server_data_obj()
    output = standup_active(server_data, input_token, input_channel_id)

    return dumps(output)

@APP.route("/standup/send", methods=['POST'])
def http_standup_send():
    """
    http_standup_send:
    Sending a message to get buffered in the standup queue, assuming a standup is currently active

    Input:
    - (JSON) {token, channel_id, message}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    channel_id = input_handle_ids(input_data["channel_id"])
    output = standup_send(server_data, input_data["token"], channel_id, input_data["message"])

    return dumps(output)

@APP.route("/admin/userpermission/change", methods=['POST'])
def http_admin_userpermission_change():
    """
    http_admin_userpermission_change:
    Given a user by their u_id, set their permission to new permissions described by permission_id

    Input:
    - (JSON) {token, u_id, permission_id}
    Output:
    - (JSON) {}
    """

    # Get input and server data
    input_data = request.get_json()
    server_data = get_server_data_obj()
    u_id = input_handle_ids(input_data["u_id"])
    permission_id = input_handle_ids(input_data["permission_id"])
    output_data = admin_userpermission_change(server_data, input_data["token"], u_id, permission_id)

    return dumps(output_data)

@APP.route("/workspace/reset", methods=['POST'])
def http_workspace_reset():
    """
    http_workspace_reset:
    Reset the workspace state

    Input:
    - (JSON) {}
    Output:
    - (JSON) {}
    """
    server_data = get_server_data_obj()
    server_data.server_data_reset()

    return dumps({})

# Additional functions
@APP.route("/admin/user/remove", methods=['DELETE'])
def http_admin_remove_user():
    """
    http_admin_remove_user:
    Remove the user from the server

    Input:
    - (JSON) {token, u_id}
    Output:
    - (JSON) {}
    """
    server_data = get_server_data_obj()
    input_data = request.get_json()
    u_id = input_handle_ids(input_data["u_id"])
    remove_user(server_data, input_data["token"], u_id)

    return dumps({})

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    """
    echo route function:
    echos the input
    """
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":

    THREAD_ONE = threading.Thread(target=save_data_period, args=(1,))
    THREAD_TWO = threading.Thread(target=message_sendlater_handler, args=())

    print("Starting the automatic saving feature of the backend server...")
    THREAD_ONE.start()
    print("Start up complete...")

    print("Starting the delayed posting feature of the backend server...")
    THREAD_TWO.start()
    print("Start up complete...")

    update_profile_image_address_port((int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

    print("")
    print("Received Termination Signal, saving the end data before exiting...")

    exit_signal_received()
