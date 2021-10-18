'''
The core functions of the helpr application.
'''
#from operator import itemgetter

# Put the global variables that hold the complete state of the application here.
dataStore = []
student_request = {}

def getdata():
    """
    global data and return it
    """
    global dataStore
    return dataStore

def getrequest():
    """
    global request number and return it
    """
    global student_request
    return student_request
    

# check_student_exist
def check_exist(zid):
    """
    Params:
      zid (str): The ZID of the student.
    Returns:
      (True) : the student made request 
      (False): not exist in the queue
    """
    data = getdata()    
    for students in data:
        if students["zid"] == zid:
            return True
    return False

# check_student_satus
def check_waiting(zid): 
    """
    Params:
      zid (str): The ZID of the student.
    Returns:
      (True) : the student are in "waiting" status 
      (False): not in "waiting" status
    """
    data = getdata()
    for students in data:
        if students["zid"] == zid:
            # if student is waiting
            if students["status"] == "waiting":
                return True    
    return False

# check_student_satus
def check_receiving(zid): 
    """
    Params:
      zid (str): The ZID of the student.
    Returns:
      (True) : the student are in "receiving" status 
      (False): not in "receiving" status
    """
    data = getdata()
    for students in data:
        if students["zid"] == zid:
            # if student is waiting
            if students["status"] == "receiving":
                return True    
            
    return False


def make_request(zid, description):
    '''
    Used by students to make a request. The request is put in the queue with a
    "waiting" status.

    Params:
      zid (str): The ZID of the student making the request.

      description (str): A brief description of what the student needs help
      with.

    Raises:
      ValueError: if the description is the empty string.

      KeyError: if there is already a request from this particular student in
      the queue.
    '''
    data = getdata()
    request = getrequest()
    
    # ValueError - description is empty string
    if not description:
        raise ValueError("empty description")
    # KeyError- already a request in the queue
    if check_exist(zid):
        raise KeyError("request exist")
        
    dic = {"zid": zid, "description": description, "status": "waiting"}
    
    data.append(dic)
    
    #if zid in request:
        #request['zid'] += 1
    #else:
        #request['zid'] = 1
    
    
def queue():
    '''
    Used by tutors to view all the students in the queue in order.

    Returns:
      (list of dict) : A list of dictionaries where each dictionary has the keys
      { 'zid', 'description', 'status' }. These correspond to the student's ZID,
      the description of their problem, and the status of their request (either
      "waiting" or "receiving").
    '''
    data = getdata()
    return data

def remaining(zid):
    '''
    Used by students to see how many requests there are ahead of theirs in the
    queue that also have a "waiting" status.

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: if the student does not have a request in the queue with a
      "waiting" status.

    Returns:
      (int) : The position as a number >= 0
    '''
    data = getdata()
    position = 0
    
    for count, students in enumerate(data):
        if students["zid"] == zid:
            # if student is not waiting
            if students["status"] != "waiting":
                raise KeyError("invalid status")
            # student is wait in the list, count how many student
            # waiting in front of this student
            else:
                for i in range(count):
                    if data[i]["status"] == "waiting":
                        position += 1
                break
    
    return position            
        
def help(zid):
    '''
    Used by tutors to indicate that a student is getting help with their
    request. It sets the status of the request to "receiving".

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: if the given student does not have a request with a "waiting"
      status.
    '''
    data = getdata()
    
    # if the given student does not have a request with "waiting" 
    if not check_exist(zid) or not check_waiting(zid):
        raise KeyError("invalid status")
    else:
        for students in data:
            if students["zid"] == zid:        
                students["status"] = "receiving"
                

def resolve(zid):
    '''
    Used by tutors to remove a request from the queue when it has been resolved.

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: if the given student does not have a request in the queue with a
      "receiving" status.
    '''
    data = getdata()
    
    if not check_exist(zid) or not check_receiving(zid):
        raise KeyError("invalid status")
    else:
        for students in data:
            if students["zid"] == zid:        
                data.remove(students)

def cancel(zid):
    '''
    Used by students to remove their request from the queue in the event they
    solved the problem themselves before a tutor was a available to help them.

    Unlike resolve(), any requests that are cancelled are NOT counted towards
    the total number of requests the student has made in the session.

    Params:
      zid (str): The ZID of the student who made the request.

    Raises:
      KeyError: If the student does not have a request in the queue with a
      "waiting" status.
    '''
    data = getdata()
    request = getrequest()
    
    if not check_exist(zid) or not check_waiting(zid):
        raise KeyError("invalid status")
    else:
        for students in data:
            if students["zid"] == zid:        
                data.remove(students)
        request['zid'] -= 1
    
    
def revert(zid):
    '''
    Used by tutors in the event they cannot continuing helping the student. This
    function sets the status of student's request back to "waiting" so that
    another tutor can help them.

    Params:
      zid (str): The ZID of the student with the request.

    Raises:
      KeyError: If the student does not have a request in the queue with a
      "receiving" status.
    '''
    data = getdata()
    
    # if the given student does not have a request with "receiving" 
    if not check_exist(zid) or not check_receiving(zid):
        raise KeyError("invalid status")
    else:
        for students in data:
            if students["zid"] == zid:        
                students["status"] = "waiting"

def reprioritise():
    '''
    Used by tutors toward the end of the help session to prioritize the students
    who have received the least help so far.

    The queue is rearranged so that if one student has made fewer non-cancelled
    requests than another student, they are ahead of them in the queue. The
    ordering is otherwise preserved; i.e. if a student has made the same number
    of requests as another student, but was ahead of them in the queue, after
    reprioritise() is called, they should still be ahead of them in the queue.
    '''
    #HINT: This function might be challenging to implement. You may wish to
    #leave it till after you test and implement the other functions.
    data = getdata()
    request = getrequest()
    
    data.sort(key = lambda k: request[k["zid"]])
    
    
    
    
def end():
    '''
    Used by tutors at the end of the help session. All requests are removed from
    the queue and any records of previously resolved requests are wiped.
    '''
    
    # clearing the queue
    # clearing the request dic
    data = getdata()
    request = getrequest()
    
    data.clear()
    request.clear()
