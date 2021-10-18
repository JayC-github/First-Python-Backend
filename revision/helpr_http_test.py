'''
HTTP tests for the helpr application
'''

import config
import urllib.request
import json
import pytest

# Do NOT change this URL! If you need to change the port number, change the
# value in config.py
BASE_URL=f"http://127.0.0.1:{config.PORT}"

def reset():
    """
    reset the workspace
    """
    data = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/end", data=data, method='DELETE', headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

def test_make_request():
    '''
    A route for helpr.make_request()

    Params: {"zid", "description"}

    Raises: BadRequest if helpr.make_request() raises a KeyError or ValueError.

    Returns: {}
    '''
    reset()
    
    data = json.dumps({"zid": "z5261536", "description": "xxx"}).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/make_request", data=data, method='POST', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    # bad request
    
    
def test_queue():
    '''
    A route for helpr.queue()

    Returns: A list in the same format as helpr.queue()
    '''
    data = json.dumps({}).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/queue", data=data, method='GET', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

def test_remaining():
    '''
    A route for helpr.remaining()

    Params: ("zid")

    Raises: BadRequest if helpr.remaining() raises a KeyError.

    Returns: { 'remaining': n } where n is an integer
    '''
    data = json.dumps({"zid": "z5261536"}).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/remaining", data=data, method='GET', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    #print(payload)

def test_help():
    '''
    A route for helpr.help()

    Params: {"zid"}

    Raises: BadRequest if helpr.help() raises a KeyError.

    Returns: {}
    '''
    data = json.dumps({"zid": "z5261536"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/help", data=data, method='POST', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    #print(payload)

def test_resolve():
    '''
    A route for helpr.resolve()

    Params: {"zid"}

    Raises: BadRequest if helpr.resolve() raises a KeyError.

    Returns: {}
    '''
    data = json.dumps({"zid": "z5261536"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/resolve", data=data, method='DELETE', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)

def test_cancel():
    '''
    A route for helpr.cancel()

    Params: {"zid"}

    Raises: BadRequest if helpr.cancel() raises a KeyError.

    Returns: {}
    '''
    data = json.dumps({"zid": "z5261536", "description": "xxx"}).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/make_request", data=data, method='POST', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    data = json.dumps({"zid": "z5261536"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/cancel", data=data, method='DELETE', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
def test_revert():
    '''
    A route for helpr.revert()

    Params: {"zid"}

    Raises: BadRequest if helpr.revert() raises a KeyError.

    Returns: {}
    '''
    data = json.dumps({"zid": "z5261536", "description": "xxx"}).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/make_request", data=data, method='POST', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    data = json.dumps({"zid": "z5261536"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/help", data=data, method='POST', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    
    data = json.dumps({"zid": "z5261536"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/revert", data=data, method='POST', headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    
def test_reprioritise():
    '''
    A route for helpr.reprioritise()

    Returns: {}
    '''
    pass


def test_end():
    '''
    A route for helpr.end()

    Returns: {}
    '''
    data = json.dumps({}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/end", data=data, method='DELETE', headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)
