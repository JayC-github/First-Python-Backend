#pylint: disable=C0301,W0105,R0914,R0915
#pylint: disable=R0801
'''
Test file for function search
When testing this function, we assume that all other functions work as expected

Needs to be run after all imported functions are tested
'''
import urllib
import json
import pytest
import constants as const

BASE_URL = f"http://127.0.0.1:{const.PORT_NUMBER}"

'''
Test case for a working search case
'''
def test_search_working(auth_http_fixture):
    """
    Pytest: testing a working search
    """

    auth_fixture = auth_http_fixture
    # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    uid2 = auth_fixture[2]['u_id']

    # create channel
    data = {
        "token": token1,
        "name": "New_Channel",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    channel_id = payload['channel_id']

    data = {
        "token": token1,
        "channel_id": channel_id,
        "u_id": uid2,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    # send messages in the channel
    data = {
        "token": token1,
        "channel_id": channel_id,
        "message": "TEST is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg1 = payload['message_id']

    data = {
        "token": token2,
        "channel_id": channel_id,
        "message": "TEST is mad!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg2 = payload['message_id']

    # make sure search shows correct list of messages
    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token1}&query_str=TEST+is+")
    payload = json.load(response)
    msglist1 = payload['messages']

    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token2}&query_str=TEST+is+")
    payload = json.load(response)
    msglist2 = payload['messages']

    assert [i['message_id'] for i in msglist1 if i['message_id'] in (msg1, msg2)] == [msg2, msg1]
    assert [i['message_id'] for i in msglist2 if i['message_id'] in (msg1, msg2)] == [msg2, msg1]


"""
Test case for messages in multiple channels
"""
def test_search_messages_multiple_chnl(auth_http_fixture):
    """
    Pytest: testing a search from multiple channels
    """

    auth_fixture = auth_http_fixture
   # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']
    token3 = auth_fixture[3]['token']
    token4 = auth_fixture[4]['token']
    uid2 = auth_fixture[2]['u_id']
    uid4 = auth_fixture[4]['u_id']

    # create channel and invite members (pub channel: user1 user2, priv channel: user2 user3 user4)
    data = {
        "token": token1,
        "name": "Pub_Channel",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    pubid = payload['channel_id']

    data = {
        "token": token3,
        "name": "Priv_Channel",
        "is_public": False,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    privid = payload['channel_id']

    # Invite users in
    data = {
        "token": token1,
        "channel_id": pubid,
        "u_id": uid2,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    data = {
        "token": token3,
        "channel_id": privid,
        "u_id": uid2,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    data = {
        "token": token3,
        "channel_id": privid,
        "u_id": uid4,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    # send messages in the channel
    data = {
        "token": token1,
        "channel_id": pubid,
        "message": "User1 is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg1 = payload['message_id']

    data = {
        "token": token2,
        "channel_id": pubid,
        "message": "User2 is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg2 = payload['message_id']

    data = {
        "token": token2,
        "channel_id": privid,
        "message": "User2 is bad!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg3 = payload['message_id']

    data = {
        "token": token3,
        "channel_id": privid,
        "message": "User3 is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg4 = payload['message_id']

    data = {
        "token": token4,
        "channel_id": privid,
        "message": "User4 is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg5 = payload['message_id']

    # make sure search shows correct list of messages
    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token1}&query_str=User")
    payload = json.load(response)
    msglist1 = payload['messages']

    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token2}&query_str=User")
    payload = json.load(response)
    msglist2 = payload['messages']

    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token3}&query_str=User")
    payload = json.load(response)
    msglist3 = payload['messages']

    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token4}&query_str=User")
    payload = json.load(response)
    msglist4 = payload['messages']

    assert [i['message_id'] for i in msglist1 if i['message_id'] in (msg1, msg2)] == [msg2, msg1]
    assert [i['message_id'] for i in msglist2 if i['message_id'] in (msg1, msg2, msg3, msg4, msg5)] == [msg5, msg4, msg3, msg2, msg1]
    assert [i['message_id'] for i in msglist3 if i['message_id'] in (msg3, msg4, msg5)] == [msg5, msg4, msg3]
    assert [i['message_id'] for i in msglist4 if i['message_id'] in (msg3, msg4, msg5)] == [msg5, msg4, msg3]

"""
Test case for empty query
"""
def test_search_empty_query(auth_http_fixture):
    """
    Pytest: testing search with empty query
    """

    auth_fixture = auth_http_fixture

    # get user details
    token1 = auth_fixture[1]['token']

    # create channel
    data = {
        "token": token1,
        "name": "New Channel",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    channel_id1 = payload['channel_id']

    data = {
        "token": token1,
        "name": "New Channel1",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    channel_id2 = payload['channel_id']

    # send messages in the channel
    data = {
        "token": token1,
        "channel_id": channel_id1,
        "message": "User1 is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg1 = payload['message_id']

    data = {
        "token": token1,
        "channel_id": channel_id1,
        "message": "User1 is goooooooooood!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg2 = payload['message_id']

    data = {
        "token": token1,
        "channel_id": channel_id1,
        "message": "All messages should pop up@",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg3 = payload['message_id']

    data = {
        "token": token1,
        "channel_id": channel_id2,
        "message": "User1 is good!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg4 = payload['message_id']

    data = {
        "token": token1,
        "channel_id": channel_id2,
        "message": "User1 is goooooooooood!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg5 = payload['message_id']

    data = {
        "token": token1,
        "channel_id": channel_id2,
        "message": "All messages should pop up@",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    msg6 = payload['message_id']

    # make sure search shows all messages for the user if query is blank string
    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token1}&query_str=")
    payload = json.load(response)
    msglist1 = payload['messages']

    assert [i['message_id'] for i in msglist1] == [msg6, msg5, msg4, msg3, msg2, msg1]

"""
Test case for empty message list
"""
def test_search_empty_msg_list(auth_http_fixture):
    """
    Pytest: testing search with empty message list
    """

    auth_fixture = auth_http_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    token2 = auth_fixture[2]['token']

    # create channels
    data = {
        "token": token1,
        "name": "New Channel",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    channel_id1 = payload['channel_id']

    data = {
        "token": token2,
        "name": "Another Channel",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    # make sure search shows no messages
    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token2}&query_str=")
    payload = json.load(response)
    msglist1 = payload['messages']

    assert [i['message_id'] for i in msglist1] == []

    # send messages with user1 on channel1
    data = {
        "token": token1,
        "channel_id": channel_id1,
        "message": "User1 only!",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    response = urllib.request.urlopen(req)
    payload = json.load(response)


    # make sure search still shows no messages for user2
    response = urllib.request.urlopen(f"{BASE_URL}/search?token={token2}&query_str=")
    payload = json.load(response)
    msglist2 = payload['messages']

    assert [i['message_id'] for i in msglist2] == []

"""
Test case for invalid token
"""
def test_search_invalid_token(auth_http_fixture):
    """
    Pytest: testing search with invalid token
    """

    auth_fixture = auth_http_fixture

    # get user details
    token1 = auth_fixture[1]['token']
    invalidtoken = '12345'

    # create channels
    data = {
        "token": token1,
        "name": "New Channel",
        "is_public": True,
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", method="POST", data=json_data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

    data = {
        "token": invalidtoken,
        "query_str": "",
    }
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/search", method="GET", data=json_data, headers={"Content-Type": "application/json"})

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
