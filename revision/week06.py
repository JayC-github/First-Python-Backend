from flask import Flask, request
from json import dumps
from werkzeug.exceptions import HTTPException
######
from time import sleep
###
import distutils.util  


app = Flask(__name__)

firstName = ''
lastName = ''

class NameException(HTTPException)
    code = 400
    message = 'xxxx is invalid'
 
@app.route('/reset', methods=['POST'])
def reset():
    global firstName, lastName
    firstName = ''
    lastName = ''
    return ""

@app.route('/info', methods=['GET'])
def info():
    uc = request.args.get('uc')
    uc = uc if is not None else False
    return dumps({
        'firstName': firstName.upper() if uc else firstName,
        'lastName': lastName.upper if uc else lastName,
    
    })

@app.route('/set', methods=['POST'])
def set():
    global firstName,     
    
    


def set_temporary():
    global firstName, lastName
    payload = request.get_json()
    
    if not payload["fisrt name"] or not paylaod["lastname"]
        raise NameException()
        
        
    firstName = payload['firstName']
    lastName = payload['lastName']
    interval = payload['interval']
    
    timer = threading.Timer(interval, reset)
    
    timer.start()
    
    return dumps({
        'firstName': payload['f']
        'lastName': payload['l']
    })
    
def test_temporary():
    data = json.dumps({
        'firstnam': 'abc',
        'lasname': 'edf',
        'interval': 2
    }).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/set_temporary", data=data, headers={xxxxxx})
    payloard = json.load(urllib.request.urlopen(req))
    
    assert payload('firstname') == 'abc'
    assert payload('lastname') == 'edf'
    
    sleep(1)
    
    query
    
    
"""
1.Rigidity: cant update or change easily
2.Fragility: software break when single change make
3.immobility: previous work is hard to use
4. viscosity: a small functionality change need big change in the code
5. opacity: difficult to understand

Extensible
reusable
maintanable
understandbale
testable

Dry -- don't repeat yourself, no repition in code
Kiss -- keep it simple and stupid 
Encapsulation


"""


import sys

if len(sys.agrv) !=2:
    sys.exit(1)
    
num = int(sys.argv[1])

if num == 2 or num == 3:
    for i in range(10, 20):
        result = i ** num
        print(f"{i} ** {num} == {result}")    
        
action  = [None, None, "squared", "cubed"]
#dictionry
action = {2: "suqred", 3: "cubed"} 
if num == 2 or num == 3:
    for i in range(10, 20):
        result = i ** num
        print(f"{i}{action[num]} = {result}")        
        
import jwt
import string

SECRET = 'applesdjkndns'

encoded_jwt = jwt.encode({'xxx':'payload'}, SECRET, algorithm='HS256')
print(jwt.decode(encode_jwt, SECRET, algorithm=['']))    


def generate_random():
    """
    Generate a random string with up to 50 characters consisting 
    of lowercase and uppercase letter.
    """    
    
    for i in range (50):
        c = random.choice(string.ascii_letters)
        result += c
    return result         
    
import random
import string


####################################################################
from math import sqrt, atan2, sin, cos 

class Point
    def __init__(self, x, y):
        #self.x = x
        #self.y = y
        self.theta = atan2(y, x)
        self.r = sqrt(x**2 + y**2)
    ## treat like a member/property
    @property
    def x(self)
        return self.r * cos(self.theta)
    
    @property
    def y(self)
        return self.r * sin(self.theta)
    
    @x.setter
    def x(self, x):
        theta = atan2(self.y, x)
        r = sqrt(x**2 + self.y**2)
        
        self.theta = theta
        self.r = r
        
        # self.theta, self.r = atan2(self.y, x), sqrt(x**2 + self.y**2)
        
    @y.setter
    def y(self, y):
        theta = atan2(self.x , y)
        r = sqrt(self.x**2 + y**2)            
        self.theta = theta
        self.r = r
        
        # self.theta, self.r = atan2(self.x, y), sqrt(self.x**2 + y**2)
        
def distance(start, end):
    return sqrt((end.x - start.x)**2 +(end.y - start.y)**2)

##################################################################

class Queue:
    def __init__(self):
        self.__entries = []
    def enqueue(self, entry):
        self.__entries.append(entry) 
    def dequeue(self):
        return self.__entires.pop(0)
    def print_entries(self):
        print(self.__entires)    
    def entries(self):
        return list(self.__entries)
    
           

def naughty():
    coffee_queue = Queue()
    coffee_queue.enqueue("Rob")
    coffee_queue.enqueue("Hayden")
    #coffee_enqueue.__entries[0] = "Cliff"
    coffee_queue.entries()[0] = "Cliff"
    
    #print(coffee_queue.__entries)
    coffe_queue.print_entries()
    print(coffe_queue.entries())
    
    
"""
Top-down thinking

Give two latitude/longitude coordinates, find out what time I would arrive at my destination if I left now. Assume I travel at the local country;s highway speed

"""    
import datetime

def curret_time():
    return datetime.datetime.now()
    
def distance_on_earth(start, end):
    pass

def highway_speed(start):
    pass

def arrive_time(start, end):
    return current_time() + distance_on_earth(start, end) / highway_speed(start)
    
# why is well designed software important 
# refactoring code --> fix code or design smells and thus make code maintanable   

######################################################################
# being pythonic --> good way to write python
# Docstrings description of function/ Parameters:<-- arguments/ Returns:
# Map, Reduce, Filter 


# Map.py

def shout(string):
    return string.upper() + "!!!!"
    
if __name__ == '__main__':
    tutors = ['Jay', 'Mercy', 'tom']
    angry_tutors = list(map(shout, tutors))
   #angry_tutors = list(map(lambda t: t.upper() + "!!!!", tutors)) 
    print(angry_tutors)
    print(tutors)    

# reduce.py
from functools import reduce

if __name__ == '__main__':
    marks = [65, 72, 81, 40, 56]
    total = reduce(lambda a,b: (a + b if b >= 50 else a), marks) # total = sum(marks)
    average = total/(len(marks))
    print(average)


# filter.py
from functions import reduce
    marks = [65, 72, 81, 40, 55]
    passing_marks = list(filter(labda m: m>= 50, marks))
    
    total = reduce(lambda a,b: a+b, passing_marks)
    average = total/ len(passing_marks)
    print(average)    
################# early.py    
class SqrtException(Exception):
    pass
 
def sqrt(num):
    if num < 0:
        raise SqrtException("NUmber cannot be <0")
    return num ** 0.5

try:
    print(sqrt(int(input())))
except SqrtException as e:
    print(e) 
    
### destructure.py  tuples
import math

def convert(x, y):
    return (math.sqrt(x**2 + y**2), math.degrees(math.atan(y/x))
    
if __name__ == '__main__':
    print("Enter x:")
    x = int(input())
    print("Enter y:")
    y = int(input())
    
    mag, dir = convert(x, y)
    print(mag, dir)
    # ignore one of the reutrn variable
    mag, _ = convert(x, y)
    print(mag)

#############################################################             
def swap(a, b):
    # c=a, a=b, b=c
    a, b = b, a        
##############################
tutor = ['aaa', 'bbb', 'vvvv', 'cccccccccc']

for idx, name in enumerate(tutor):
    print(f"{idx+1}:{name}")        
       
#########################################################
SDLC -- User stories
Requirements
elicitation/analysis/specification/validation
A method of requirements engineering ued to inform the development

#As a <type of user>, I want < soe goal> so that <reason>
As a student, I want to purchasing a parking pass so that I can drive to school.
user-goal focused.
User stories- Activity

Example:
# TODO app

- As a user, I want to add a task so that I don't have to remember to do it
- As a user, I want to mask a task as done, such that I dont have to be reminded again
INVESET
I = independant as possible
N = Negotiable avoid details, simple
V = Valuable: 
E
S = short
T = testable



