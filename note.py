week01

# pipeline

SDLC(kahoot)
software development life cycle

###
requirements analysis-> design -> development -> testing -> 
deployment -> maintenance

1. functional/ non-functional compoents
a specific service that the system should provide
send notification

how the system achieve that, performance characteristic
send email no later than 30 minss

2. deployment = ship it
3. maintenance = monitor

# Run in the terminal
python3
print("Hello")
==>
python3 -c 'print("Hello")'

# print and strings
name = "Jay"
age = 20
print(name + "," + str(age))
print(f"{name},{age}")
print(type(name))
print(type(age))

sentence = "my"
sentence += "dick is big"
print(sentence)
print(sentence * 10)

# control structures, argc/argv
import sys
argc = len(sys.argv)
print(argc)
print(sys.argv[0])
print(sys.argv[1])

# strings
name = ["Mercy", "Mer", "cYCY"]
name.append("Jay")

for names in name:
    print(names)

for i in range(len(name)):
    print(name[i])    

# tuple

x = 5
y = 6
point = (x,y)
print(point)

a, b = point
print(str(a) + "," + str(b))
print(f"{a}, {b}")
print("{}, {}".format(a, b))

# enumerate
name = ["Mercy", "Mer", "cYCY"]
name.append("Jay")

for i, names in enumerate(name):
    print(i)
    print(names)

# Git
clone/status/diff/add/commit/push/pull
log/pull/merge

# run pytest-3
# pytest-3 -k

import pytest

def sum(a, b):
    return a + b
    
def test_sum1():
    assert sum(1, 2) == 3    

# tuple and list are differnet
# list
a = [1, 2, 3]
# tuple, u can't append or change the element inside
# pack a tuple
t = (1, 2, 3)
# unpack a tuple
x, y, z = t


week02
# agile
1. Elication
2. analysis
3. specification
4. validation

# dictionaries
student = {}
student["name"] = "Jay"
student["age"] = 20
student["height"] = "185cm"


print(student)

userData = [
    {
        "name": "Jay",
        "age": 18,
        "Height": 1,
    }, {
        "name": "Jay1",
        "age": 12,
        "Height": 1,
    }, {
        "name": "Jay3",
        "age": 13,
        "Height": 1,
    },
]

userDataa = {
        "name": "Jay",
        "age": 18,
        "Height": 1,
    }

for user in userDataa.keys():
    print(user)

import sys
def sqrt(x):
    if x < 0:
        raise Exception("*****************")
    return x**0.5
if __name__ == '__main__':
    inputNum = int(input("plz enter an integer:")) 
    try:
        print(sqrt(inputNum))
    except Exception as e:
        print(f"u put and negative integer, fuck{e}")    

import sys
import pytest
def sqrt(x):
    if x < 0:
        raise ValueError("xxxxxxxxxxxxxxxx")
    return x**0.5

def test_sqrt_ok():
    assert sqrt(1) == 1

def test_sqrt_bad():
    with pytest.raises(Exception/ValueError):
        sqrt(-1)
# standups        
1. what did i do?
2. what problems did i face?
3. what I'm going to do?  

Asynchronous Stand-ups
pro: no need to find a suitable time for everyone
con: missed updates, less personal

Test-Driven-Development
(TDD)
Writing tests before the implementation
Write only enough code to make the next test pass


# week03 objects
from datetime import date
print(date.today().ctime())

class Student:
    def __init__(self, zid, name):
        self.zid = zid
        self.name = name
        self.year = 1

    def advance_year(self):
        self.year += 1

    def email_address(self):
        return self.zid + "@unsw.edu.au"

rob = Student("z3254687", "Robert")
hayden = Student("z5261536", "Hay")

print(rob.year) 1
Student.advance_year(rob)
print(rob.year) 2
rob.advance_year()
print(rob.year) 3


print(rob.email_address())
print(rob.name)

verification:
The sys has been built right
Validation:
The right system has been built

Unit testing - whitebox by software engineers
integration testing - whitebox or balckbox
system testing: black-box by independent testers
acceptance testing: black-box by user/customers

# coverage

branch coverage >> statement coverage

python3-coverage run --source=. -m pytest
python3-coverage report
python3­-coverage html

# week04 http/flask
computer networks --> web --> internet
network -> a group of computers that can communicate
internet -> infrastructer for networking computers around the entire world
world wide web -> a system of documents and recources link like URLs

# flask
from flask import Flask, request
from json import dumps

APP = Flask(__name__)

@APP.route("/")
def hello():
    return "Hello world?"

@APP.route("/hello")
def mer():
    return "I love Mercy!"   
@APP.route("/get", methods=['GET'])
def get():
    data = request.get_json()
    return dumps({
        data["xxxx"]
    })

@APP.route("/xxx", methods=["POST"])
def login():
    data = request.get_json()
    return dumps(auth_login(data["email"], data["password"]))   
    
if __name__ == "__main__":
    APP.run()    
    
    
# flask testing
import urllib
import json
import pytest

BASE_URL = 'http://127.0.0.1:5000'    
    
data = json.dumps({'name': 'Jay'}).encode()

req = urllib.request.Request(f"{BASE_URL}/name/add", method='POST', data=data, headers={'Content-Type': 'application/json'})

payload = json.load(urllib.request.urlopen(f"{BASE_URL/names}"))    
assert payload == {'names': ['Jay']}

# API application programming interface
# 4 methods of CRUD
POST  create
GET   read
PUT   update
DELETE  delete/remove
# state/auth

authentication: process of verifying the identity of a user
registers/logs in 

authorisation: process of verifying an identity's access privileges
"token"

# storing data
pickle_it.py

import pickle

DATA_STRUCTURE = {
    'names': [
        {
            'first' : 'Bob',
            'last' : 'Carr'
        },
        {
            'first' : 'Julia',
            'last' : 'Gillard'
        },
}

with open('export.p', 'wb') as FILE:
    pickle.dump(DATA_STRUCTURE, FILE)
   #json.dump(data, file)
unpickle_it.py

import pickle

DATA = pickle.load(open("export.p", "rb")) # alternative way
print(DATA)

import json

with open('export.json', 'r') as FILE:
    DATA = json.load(FILE)
    print(DATA)

# http testing
data = json.dumps({
        'hello' : 'world'
    }).encode('utf-8')

req = urllib.request.Request(f"{BASE_URL}/set",data=data,headers={'Content-Type': 'application/json'})

payload = json.load(urllib.request.urlopen(req))

#HTTP STATUS
200 - succcess
405 - valid routes but wrong method(method now allowds)
404 - invalid routes
403 - no permission - not allowed to access
500 - server problem, no invalid token-> server get fucked with valid request
400 - does not meet specific criteria bad request

# week06 design principles
design smell:
Rigidity: Tendency to be too difficult to change
Fragility: Tendency for software to break when
single change is made
Immobility: Previous work is hard to reuse or move
Viscosity: Changes feel very slow to implement
Opacity: Difficult to understand
Needless complexity:  Things done more complex
than they should be
Needless repetition: Lack of unified structures
Coupling: Interdependence between components

DRY -- don't repeat urself (reducing repitition in the code)
kiss -- keep it simple and stupid
top-down thinking -- you aren't gonna need it

Acceptance Tests are tests that are performed to
ensure acceptance criteria have been met -- black box

import sys

if len(sys.argv) != 2:
    sys.exit(1)
    
num = int(sys.argv[1])

for i in range(10, 20):
    result = i ** num
    print(f"{i} ** {num} = {result}")

### being pythonic

1. Docstrings
2. map/reduce/filter/lambda

### map: creates a new list with the results of calling a provided
function on every element in the given list

def shout(string):
    return string.upper() + "!!!!"
if __name__ == '__main__':
    tutors = ['Simon', 'Teresa', 'Kaiqi', 'Michelle']
    shout_tutors = list(map(shout, tutors))
    print(shout_tutors)        

### reduce: executes a reducer function (that you provide) on
each member of the array resulting in a single output value

# importing functools for reduce() 
import functools 
  
# initializing list 
lis = [ 1, 3, 5, 6, 2] 

def sum_two(a, b):
    return a + b

# using reduce to compute sum of list 
print ("***The sum of the list elements is : ",end="") 
print (functools.reduce(sum_two, lis)) 

  
# using reduce to compute sum of list 
print ("The sum of the list elements is : ",end="") 
print (functools.reduce(lambda a,b : a+b, lis)) 
  
# using reduce to compute maximum element from list 
print ("The maximum element of the list is : ",end="") 
print (functools.reduce(lambda a,b : a if a > b else b, lis)) 



### filter: creates a new array with all elements that pass the
test implemented by the provided function

marks = [64,73,81,49,43,50]

passing_marks = list(filter(lambda x: x >= 50, marks))
print(passing_marks)    

3. exceptions > early returns
4. enumerate

a = int(input("enter a number:"))
b = int(input("enter another number:"))

jay, mercy = a,b

print(jay)
print(mercy)

players = ["kobe", "lebron", "jordan", "wade"]

for i, player in enumerate(players):
    print(f"{i}, {player}")
    
    
#INVEST
I = Independent: user story could be developed
independently and delivered separately
N = Negotiable: avoid too much detail.
V = Valuable: must hold some value to the client
E = Estimable: we'll get to this in a later lecture
S = Small: user story should be small
T = Testable

def bubblesort(nums):
    nums = nums.copy()
    for i in range(len(nums)):
        for j in range(len(nums) - 1 - i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]

    return nums
    
    
print(bubblesort([5,1,2,9,8]))    

######## 9 python generators and iterators  
An iterator has __iter__() and __next()__ methods.
Iterables have __iter__() methods

animals = ["dog", "cat", "sheep", "pig"]

ai = iter(animals)

for item in ai:
    print(item + "aaaaaaaa")   

for _ in range(len(animals)):
    print(next(ai) + "********")

# simple generators
def simple_generator():
    print("Hello")
    yield 1
    print("Nice to meet you")
    yield 2 
    print("I am a generator")

s = simple_generator()
print(next(s))
print(next(s))

# 9.2 software complexity     
# essential, accidentials
# cyclomatic complexity
Value(graph) = e - n + 2
             edges - nodes + 2

a[start:stop]  # items start through stop-1
a[start:]      # items start through the rest of the array
a[:stop]       # items from the beginning through stop-1
a[:]           # a copy of the whole array

a[start:stop:step] # start through not past stop, by step

a[-1]    # last item in the array
a[-2:]   # last two items in the array
a[:-2]   # everything except the last two items

a[::-1]    # all items in the array, reversed
a[1::-1]   # the first two items, reversed
a[:-3:-1]  # the last two items, reversed
a[-3::-1]  # everything except the last two items, reversed

## pickle file

1 # Save a dictionary into a pickle file.
2 import pickle
3 
4 favorite_color = { "lion": "yellow", "kitty": "red" }
5 
6 pickle.dump(favorite_color, open( "save.p", "wb" ))

1 # Load the dictionary back from the pickle file.
2 import pickle
3 
4 favorite_color = pickle.load(open( "save.p", "rb" ))
5 # favorite_color is now { "lion": "yellow", "kitty": "red" }
   
# how to do testing
@given(strategies.integers(min_value=1, max_value=10000))
def test_radom(num):
    assert divisors(num) == divisors(num)
    for i in divisors(num):
        assert num % i == 0
        
@given(strategies.integers(max_value=0))        
def test_nonpositive(num):
    with pytest.raises(ValueError):
        divisors(num)    
# how to chek if an input is not a positive integer
if type(num) is not int or num <= 0:
    dksjhfsdk
# how to generate prime factors of n
from divisors import divisors

# You may find this helpful
def is_prime(n):
    return n != 1 and divisors(n) == {1, n}

def factors(n):
    '''
    A generator that generates the prime factors of n. For example
    >>> list(factors(12))
    [2,2,3]

    Params:
      n (int): The operand

    Yields:
      (int): All the prime factors of n in ascending order.

    Raises:
      ValueError: When n is <= 1.
    '''
    if type(n) is not int or n <= 1:
        raise ValueError(f"{n} does not have a prime factors")
    
    num = n
    for i in range(1, n + 1):
        if is_prime(i):
            while num % i == 0:
                yield i
                num = num/i
#kahhot
1. sdlc requirements analysis-> design -> development -> testing -> 
deployment -> maintenance
2. tuples and list are different in behavior and functionality
3. kiss: keep it simple and stupid
4. What do we call it when our data state exists longer than the process using it? -->presistence
5. authentication: process of verifying the identity of a user
7. web is part of the internet, the internet is a type of network
8. www:A system of documents and resources linked together, accessible via URLs
9. API clients: arc and postman
10. POST  create, GET   read, PUT   update, DELETE  delete/remove
11. asynchronous communication: email ur manager instead of doing a standup meeting
12. Individuals and interactions over processes and tools
    Working software over comprehensive documentation
    Customer collaboration over contract negotiation
    *Responding to change over following a plan
13. Unit testing - whitebox by software engineers
    integration testing - whitebox or balckbox
    system testing: black-box by independent testers
    acceptance testing: black-box by user/customers
14. Statement coverage measures what statement are executed    
15. state diagram: transition 
16. f(f(x)) = f(x) idempotent
17. exception:Action that disrupts the normal flow of a program
18. elicitation->anlysis->specification->validation
23. The first argument of every instance method in a class refers to the current instance. --> self
25. integration Testing focuses on checking data communication amongst these modules.
26. protocal path params prefix 
27. high cohesion "The degree to which elements of a module belong together." element belong to each other in one module 
 coupling-> dependcy betwwen modules should be less
28. systemetical complexity and accidental complexity
32. black box testing: Writing tests based only on the specification and not the implementation


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
