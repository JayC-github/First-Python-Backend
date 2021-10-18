"""
A file to test all data structures for iteration 2
Will test:
- sessions_class
- user_class
- message_class
- reacts_class
- server_data_class
- channel_class
"""

import pytest
import constants as constants
from channel_class import Channel
from message_class import Message
from reacts_class import Reacts
from server_data_class import Server_data
from sessions_class import Sessions
from user_class import User




def test_user_class():
    # Initialize essential data:
    
    u_id = 510444
    email = "steven@gmail.com"
    password = "HASHED_PASSWORD"
    name_first = "Steven"
    name_last = "Yang"
    handle = "stevenyang"
    global_permission_id = constants.PERMISSION_GLOBAL_OWNER
    testUser = User(u_id, email, password, name_first, name_last, handle, global_permission_id)
    
    # Getters
    assert testUser.u_id == 510444
    assert testUser.email == "steven@gmail.com"
    assert testUser.password == "HASHED_PASSWORD"
    assert testUser.name_first == "Steven"
    assert testUser.name_last == "Yang"
    assert testUser.handle == "stevenyang"
    assert testUser.global_permission_id == constants.PERMISSION_GLOBAL_OWNER
    
    # Setters
    testUser.u_id = 1010101
    assert testUser.u_id == 1010101
    testUser.email = "richard@gmail.com"
    assert testUser.email == "richard@gmail.com"
    testUser.password = "NOTHASH"
    assert testUser.password == "NOTHASH"
    testUser.name_first = "Richard"
    assert testUser.name_first == "Richard"
    testUser.name_last = "Park"
    assert testUser.name_last == "Park"
    testUser.handle = "richardpark"
    assert testUser.handle == "richardpark"
    testUser.global_permission_id = constants.PERMISSION_GLOBAL_MEMBER
    assert testUser.global_permission_id == constants.PERMISSION_GLOBAL_MEMBER
    
    
    #release_user_info
    assert(testUser.release_user_info() == {
        "u_id": 1010101,
        "email": "richard@gmail.com",
        "name_first": "Richard",
        "name_last": "Park",
        "handle_str": "richardpark" ,
    })
    

    # Test is owner of slackr
    assert testUser.is_owner_of_slackr() == False
    assert testUser.is_member_of_slackr()
    testUser.global_permission_id = constants.PERMISSION_GLOBAL_OWNER
    assert testUser.is_owner_of_slackr()
    assert testUser.is_member_of_slackr() == False
    
    
def test_sessions_class():
    
    s_list = Sessions()
    test_token = "AHJFAHJKRHKA"
    test_u_id = 14
    assert s_list.is_token_active(test_token) == False
    assert s_list.is_user_active(test_u_id) == False
    
    token1 = "TOKEN1"
    u_id1 = 1
    s_list.create_active_session(u_id1, token1)
    assert s_list.is_token_active(token1)
    assert s_list.is_user_active(u_id1)
    
    assert s_list.get_user_tokens(u_id1) == [token1]
    assert s_list.get_token_user(token1) == u_id1
    assert s_list.get_num_active_sessions() == 1
    
    token11 = "TOKEN10"
    s_list.create_active_session(u_id1, token11)
    assert s_list.is_token_active(token11)
    assert s_list.is_user_active(u_id1)
    
    assert s_list.get_user_tokens(u_id1) == [token1, token11]
    assert s_list.get_token_user(token11) == u_id1
    assert s_list.get_num_active_sessions() == 2
    
    token2 = "TOKEN2"
    u_id2 = 2
    s_list.create_active_session(u_id2, token2)
    assert s_list.is_token_active(token2)
    assert s_list.is_user_active(u_id2)
    
    assert s_list.get_user_tokens(u_id2) == [token2]
    assert s_list.get_token_user(token2) == u_id2
    assert s_list.get_num_active_sessions() == 3
    
    s_list.end_active_session(token11)
    assert s_list.get_num_active_sessions() == 2
    assert s_list.is_token_active(token11) == False
    assert s_list.is_user_active(u_id1)
    
    s_list.clear_all_sessions()
    assert s_list.get_num_active_sessions() == 0
    
    
    
    
    
def test_message_class():
    message_id = 0
    message = "This is a test message"
    created_by = 4
    timestamp = 12414141
    
    msg_test = Message(message_id, message, created_by, timestamp)
    
    assert msg_test.message_id == message_id
    assert msg_test.message == message
    assert msg_test.created_by == created_by
    assert msg_test.time_created == timestamp
    assert msg_test.is_pinned == False
    
    react_list = msg_test.get_list_of_reacts()
    assert len(react_list) == 1
    
    assert msg_test.does_reaction_type_exist(1)
    assert msg_test.does_reaction_type_exist(2) == False
    
    reacts = msg_test.get_reacts_by_react_id(1)
    assert reacts.react_id == 1
    assert(len(reacts.get_user_reaction_list()) == 0)
    
    msg_test.add_new_react_type(2)
    react_list = msg_test.get_list_of_reacts()
    assert len(react_list) == 2
    
    reacts2 = msg_test.get_reacts_by_react_id(2)
    assert reacts2.react_id == 2
    assert len(reacts2.get_user_reaction_list()) == 0

    msg_test.add_new_reaction(1, 5)
    assert len(reacts.get_user_reaction_list()) == 1
    
    msg_test.add_new_reaction(1, 9)
    assert len(reacts.get_user_reaction_list()) == 2
    
    assert msg_test.has_user_reacted(1,5)
    assert msg_test.has_user_reacted(1,9)
    assert msg_test.has_user_reacted(2,5) == False
    assert msg_test.has_user_reacted(5,5) == False
    
    
    msg_info = msg_test.pack_message_info(5)
    assert msg_info == {
        "message_id": 0,
        "message": "This is a test message",
        "u_id": 4,
        "time_created": 12414141,
        "reacts": [{
            "react_id": 1,
            "u_ids": [5, 9],
            "is_this_user_reacted": True,
        }, {
            "react_id": 2,
            "u_ids": [],
            "is_this_user_reacted": False,
        }],
        "is_pinned": False,
    }
    
    # Test setters
    msg_test.message_id = 1
    msg_test.message = "TEST"
    msg_test.created_by = 5
    msg_test.time_created = 1234
    msg_test.is_pinned = True
    
    msg_info = msg_test.pack_message_info(4)
    assert msg_info == {
        "message_id": 1,
        "message": "TEST",
        "u_id": 5,
        "time_created": 1234,
        "reacts": [{
            "react_id": 1,
            "u_ids": [5, 9],
            "is_this_user_reacted": False,
        }, {
            "react_id": 2,
            "u_ids": [],
            "is_this_user_reacted": False,
        }],
        "is_pinned": True,
    }
    
    
    msg_test.remove_reaction(1, 5)
    assert len(reacts.get_user_reaction_list()) == 1
    assert msg_test.has_user_reacted(1,5) == False
    
    msg_test.react_clear(1)
    assert len(reacts.get_user_reaction_list()) == 0
    
    msg_test.remove_react_type(1)
    react_list = msg_test.get_list_of_reacts()
    assert len(react_list) == 1
    
    
    
    
def test_channel_class():
    channel_id = 213
    name = "test_channel" 
    created_by = {
        "u_id": 1, 
        "name_first": "Richard", 
        "name_last": "Park",
    }
    
    
    channel = Channel(channel_id, name, created_by, False)
    
    # Test getters
    assert channel.channel_id == 213
    assert channel.name == "test_channel"
    assert channel.is_public == False
    
    # Test setters
    channel.channel_id = 123
    channel.name = "TEST"
    channel.is_public = True
    assert channel.channel_id == 123
    assert channel.name == "TEST"
    assert channel.is_public == True
    
    assert channel.get_owner_list() == [{
        "u_id": 1,
        "name_first": "Richard",
        "name_last": "Park",
    }]
    
    assert channel.get_member_list() == [{
        "u_id": 1,
        "name_first": "Richard",
        "name_last": "Park",
    }]
    
    assert channel.is_user_owner(2) == False
    assert channel.is_user_owner
    assert channel.is_user_member(2) == False
    assert channel.is_user_member(1)
    
    owner2 = {
        "u_id": 2,
        "name_first": "Richard",
        "name_last": "Park",
    }
    channel.add_owner(owner2)
    assert channel.is_user_owner(2)
    assert channel.is_user_member(2)
    assert channel.get_num_members() == 2
    assert channel.get_num_owners() == 2
    
    channel.remove_owner(2)
    assert channel.is_user_owner(2) == False
    assert channel.is_user_member(2)
    assert channel.get_num_members() == 2
    assert channel.get_num_owners() == 1
    assert len(channel.get_member_list()) == 2
    assert len(channel.get_owner_list()) == 1
    
    member1 = {
        "u_id": 3,
        "name_first": "David",
        "name_last": "Park",
    }
    
    channel.add_member(member1)
    assert channel.is_user_owner(3) == False
    assert channel.is_user_member(3)
    assert channel.get_num_members() == 3
    assert channel.get_num_owners() == 1
    assert len(channel.get_member_list()) == 3
    assert len(channel.get_owner_list()) == 1
    
    
    channel.remove_member(1)
    assert channel.is_user_owner(1) == False
    assert channel.is_user_member(1) == False
    assert channel.get_num_members() == 2
    assert channel.get_num_owners() == 0
    assert len(channel.get_member_list()) == 2
    assert len(channel.get_owner_list()) == 0
    
    channel.add_owner(member1)
    assert channel.is_user_owner(3)
    assert channel.is_user_member(3)
    assert channel.get_num_members() == 2
    assert channel.get_num_owners() == 1
    assert len(channel.get_member_list()) == 2
    assert len(channel.get_owner_list()) == 1
    
    assert len(channel.get_message_list()) == 0
    
    
    message_id = 123
    message = "TEST1"
    created_by = 3
    channel.add_message(message_id, message, created_by)
    
    message_id2 = 133
    message2 = "TEST2"
    created_by2 = 2
    channel.add_message(message_id2, message2, created_by2)
    
    message_list = channel.get_message_list()
    assert len(message_list) == 2
    assert message_list[0].message_id == 133
    assert message_list[1].message_id == 123
    
    
    assert channel.does_message_exist(123)
    assert channel.does_message_exist(144) == False
    
    message_list2 = channel.get_message_range(0, -1)
    assert len(message_list2) == 2
    assert message_list2[0].message_id == 133
    assert message_list2[1].message_id == 123
    
    message_list3 = channel.get_message_range(0, 1)
    assert len(message_list3) == 1
    assert message_list3[0].message_id == 133
    
    message_list4 = channel.get_message_range(0, 2)
    assert len(message_list4) == 2
    assert message_list4[0].message_id == 133
    assert message_list4[1].message_id == 123
    
    message_list5 = channel.message_search("TEST")
    assert len(message_list5) == 2
    assert message_list5[0].message_id == 133
    assert message_list5[1].message_id == 123
    
    message_list6 = channel.message_search("1")
    assert len(message_list6) == 1
    assert message_list6[0].message_id == 123
    
    
    assert channel.pack_channel_details() == {
        "name": "TEST",
        "owner_members": [{
            "u_id": 3,
            "name_first": "David",
            "name_last": "Park",
        }],
        "all_members": [{
            "u_id": 2,
            "name_first": "Richard",
            "name_last": "Park",
        }, {
            "u_id": 3,
            "name_first": "David",
            "name_last": "Park",
        }],
    }
    
    
    
    
def test_server_data_class():
    server = Server_data()
    
    assert server.next_u_id == 5000000
    assert server.next_channel_id == 0
    assert server.next_message_id == 0
    
    # GETTER/SETTER test
    server.next_u_id = 4000000
    assert server.next_u_id == 4000000
    server.next_channel_id = 1000
    assert server.next_channel_id == 1000
    server.next_message_id = 2000
    assert server.next_message_id == 2000
    
    
    # Session object
    sessions = server.get_sessions_list()
    assert sessions.get_num_active_sessions() == 0
    
    assert len(server.get_user_list()) == 0
    assert len(server.get_channel_list()) == 0
    
    # New Users
    assert server.num_users() == 0
    
    u_email = "richard@gmail.com"
    u_password = "12345"
    u_name_first = "Richard"
    u_name_last = "Park"
    u_handle = "richardpark"
    u_global_permission_id = constants.PERMISSION_GLOBAL_OWNER
    
    u_id = server.new_user(u_email, u_password, u_name_first, u_name_last, u_handle, u_global_permission_id)
    assert server.num_users() == 1
    assert u_id == 4000000
    assert server.next_u_id == 4000001
    
    assert server.does_user_exist(u_id)
    assert server.does_email_exist(u_email)
    assert server.does_handle_exist(u_handle)
    
    user = server.get_user_by_id(u_id)
    assert user.u_id == 4000000
    assert user.email == "richard@gmail.com"
    assert user.name_first == "Richard"
    assert user.name_last == "Park"
    assert user.handle == "richardpark"
    
    user1 = server.get_user_by_email(u_email)
    assert user.u_id == user1.u_id
    assert user.email == user1.email
    assert user.name_first == user1.name_first
    assert user.name_last == user1.name_last
    assert user.handle == user1.handle
    
    u_email = "steven@gmail.com"
    u_password = "54321"
    u_name_first = "Steven"
    u_name_last = "Yang"
    u_handle = "stevenyang"
    u_global_permission_id = constants.PERMISSION_GLOBAL_MEMBER
    
    u_id = server.new_user(u_email, u_password, u_name_first, u_name_last, u_handle, u_global_permission_id)
    assert server.num_users() == 2
    assert u_id == 4000001
    assert server.next_u_id == 4000002
    
    assert server.pack_all_user_infos() == [{
        "u_id": 4000000,
        "email": "richard@gmail.com",
        "name_first": "Richard",
        "name_last": "Park",
        "handle_str": "richardpark",
    }, {
        "u_id": 4000001,
        "email": "steven@gmail.com",
        "name_first": "Steven",
        "name_last": "Yang",
        "handle_str": "stevenyang",
    }]
    
    server.user_list_clear()
    assert server.num_users() == 0
    assert server.next_u_id == 4000002
    
    
    
    
    # CHANNELS!
    u_email = "richard@gmail.com"
    u_password = "12345"
    u_name_first = "Richard"
    u_name_last = "Park"
    u_handle = "richardpark"
    u_global_permission_id = constants.PERMISSION_GLOBAL_OWNER
    
    u_id1 = server.new_user(u_email, u_password, u_name_first, u_name_last, u_handle, u_global_permission_id)
    
    u_email = "steven@gmail.com"
    u_password = "54321"
    u_name_first = "Steven"
    u_name_last = "Yang"
    u_handle = "stevenyang"
    u_global_permission_id = constants.PERMISSION_GLOBAL_MEMBER
    
    u_id2 = server.new_user(u_email, u_password, u_name_first, u_name_last, u_handle, u_global_permission_id)
    
    assert server.num_channels() == 0
    channel_name = "TEST1"
    channel_name2 = "TEST2"
    
    channel_id1 = server.create_channel(channel_name, u_id1, True)
    assert server.num_channels() == 1
    assert server.does_channel_exist(1000)
    
    channel_id2 = server.create_channel(channel_name2, u_id1, True)
    assert server.num_channels() == 2
    assert channel_id2 == 1001
    assert server.does_channel_exist(1001)
    assert server.does_channel_exist(1000)
    
    channel = server.get_channel_by_id(1001)
    assert channel.name == "TEST2"
    assert channel.channel_id == 1001
    
    server.delete_channel(1001)
    assert server.num_channels() == 1
    
    
    server.clear_channels()
    assert server.num_channels() == 0
    
    server.server_data_reset()
    assert server.num_channels() == 0
    assert server.num_users() == 0
    sessions = server.get_sessions_list()
    assert sessions.get_num_active_sessions() == 0
    
    assert server.next_u_id == 5000000
    assert server.next_channel_id == 0
    assert server.next_message_id == 0
    
