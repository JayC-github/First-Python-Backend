'''
Tests for the core functionality of the helpr application
'''
import pytest
# Don't change this import line below. If your tests are black-box tests then
# you don't require any more functions from the module than these
from helpr import make_request, queue, remaining, help, resolve, cancel, revert, reprioritise, end

def test_sanity():
    '''
    A simple sanity test of the system.
    '''
    # DO NOT CHANGE THIS TEST! If you feel you have to change this test then
    # your functions have not been implemented correctly.
    student1 = "z1234567"
    description1 = "I don't understand how 'global' works in python"
    student2 = "z7654321"
    description2 = "What's the difference between iterator and iterable?"

    # Queue is initially empty
    assert queue() == []
    
    # Student 1 makes a request
    make_request(student1, description1)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"}]
    assert remaining(student1) == 0

    # Student 2 makes a request
    make_request(student2, description2)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    assert remaining(student1) == 0
    assert remaining(student2) == 1

    # Student 1 gets help
    help(student1)
    assert queue() == [{"zid": student1, "description": description1, "status": "receiving"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    # Student 2 is now the only student "waiting" in the queue, so they have no
    # one remaining in front of them
    assert remaining(student2) == 0

    # Student 1 has their problem resolved
    resolve(student1)
    # Only student 2 is left in the queue
    assert queue() == [{"zid": student2, "description": description2, "status": "waiting"}]

    # Student is helped and their problem is resolved
    help(student2)
    resolve(student2)
    assert queue() ==[]

    # End the session
    end()

def test_make_requet_error():
    '''
    test for error in make request function
    '''
    student1 = "z5263516"
    description1 = ""
    student2 = "z5263517"
    description2 = "What's the difference between c and python"

    # test empty string
    with pytest.raises(ValueError):
        make_request(student1, description1)
    
    # Student 2 makes a request
    make_request(student2, description2)
    
    # request again to test request exist
    with pytest.raises(KeyError):
        make_request(student2, description2)
    
    # End the session
    end()

def test_remaining_error():
    """
    test for all the rests errors
    """      
    student1 = "z1234567"
    description1 = "I don't understand how 'global' works in python"
    student2 = "z7654321"
    description2 = "What's the difference between iterator and iterable?"
    
    make_request(student1, description1)
    make_request(student2, description2)
    
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    
    # student 2 cancle request
    cancel(student2)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"}]
    
    # student 2 make request again
    make_request(student2, description2)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    
    assert remaining(student1) == 0
    
    # help student1, status change from waiting to recieving
    help(student1)
    assert queue() == [{"zid": student1, "description": description1, "status": "receiving"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    
    # student1 is receiving not waiting
    with pytest.raises(KeyError):
        remaining(student1)
    
    # student1 is receiving, can't help
    with pytest.raises(KeyError):
        help(student1)    
    # student1 is receiving, can't cancel
    with pytest.raises(KeyError):
        cancel(student1)  
    # tutor too busy, revert student 1
    revert(student1)
    assert queue() == [{"zid": student1, "description": description1, "status": "waiting"},
                       {"zid": student2, "description": description2, "status": "waiting"}]
    
    # tutor can't revert student 1 again
    with pytest.raises(KeyError):
        revert(student1) 
    
    # student2 is waiting, can't resolve
    with pytest.raises(KeyError):
        resolve(student2)   
    
