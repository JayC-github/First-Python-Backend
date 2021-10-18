# iterator is like a pointer
animals = ["dog", "cat", "sheep"]
# sets are unorder
animals = {"dog", "cat", "sheep"}
# it's had start to end
animals = {"dog": 1, "cat": 2, "chicken":5, "sheep": 10}

animal_iterator = iter(animals)

next(animal_iterator)
next(animal_iterator)

# for loops is like an iterator
for a in animals:
    print(a)

# iterators
class Squares:
    def __init__(self):
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.i += 1
        if self.i >= 1000:
            raise StopIteration
        return self.i*self.i
        

# generators 
def squares():
    i = 0
    while i < 1000:
        i += 1
        yield i * i


# keep looping till 1000^2
# for loop will call next for u
# iterator = Squares
# while True:
#   try:
#       print(next(iteratior))
#       print(next)

for s in Squares():
    print(s)    
        
squares_interator = Squares()
next(squares_iterator)  == 1
next(squares_iterator)  == 4
next(squares_iterator)  == 9
next(squares_iterator)  == 16

# list are iterables but not iterator
# iterable only have __iter__() but not __next__()


# simple generators
def simple_generator():
    print("Hello")
    yield 1
    print("Nice to meet you")
    yield 2 
    print("I am a generator")

for i in simple_generator():
    print(i)

    
i = simple_generator()
next(i)
Hello
1
next(i)
Nice to meet you
2
next(i)
I am a generator
StopIteration   

# Fibonacii
class Fibonacci():
    def __init__(self):
        self.a = 0
        self.b = 1
    def __iter__(self):
        return self
    def __next__(self):
        c = self.a + self.b
        self.a = self.b
        self.b = c
        return self.a 
        
def fibonacci():
    a = 1
    b = 1
    while True:
        yield a
        a, b = b, a + b
i = 0
for f in fibonacci():
    print(f)
    i += 1
    if i > 100:
        break        
"""        
def with_next(iterator):
    a = next(iterator)
    for b in iterator:
        yield a,b
        a = b

def fibonacci():
    yield 1
    yield 1
    f_n2 = fibonacci()
    f_n1 = fibonacci()
    next(f_n1)
   # future = with_next(fibonacci()) 
    
    for f in map(lambda a,b: a+b, f_n2, f_n1)
   #yield from         
"""
# software complexity
# No silver Bullet  essential/accidental
# essential ->things requires by client/user
# fundamentally can't be removed, but can managed with good software design

# accidental -> generating or parsing data 
# smart user of libraries, standards, etc
# hard to remove entirely
# how to measure complexity
# coupling V(G) = e - n + 2
#               edges nodes
# pylint --load-plugings=pylint.extensions.mccabe xxx.py
# safety -- protection from accidental misuse
# security --  protection from deliberate misuse
# static -- pylint statically checks run time/ the variables are initialised before they're used
# dynamic -- check when execute
# memory safety-- c is not memory safe, python is

# python convention to handle the error, easier to understand
# easier to ask for forgiveness than permission
def eafp(a, b, i, d):
    try:
        return b[a[i]]
    except KeyError:
        return d
# look before you leap like C, convention for avoiding errors
def lbyl(a,b,i,d):
    if i in a:
        i2 = a[i]
        if i2 in b:
            return b[i2]
        else:
            return d
    else:
        return d            
            
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxx mypy xxx.py
from typing import List, Optional, TypeVar, Iterable

T = TypeVar("T")               # Iterable[T]
def count(needle: T, haystack:List[T]) -> int:
def count(needle: str, haystack: List[str]) -> int:
    copies = 0
    for value in haystack:
        if needle == value:
            copies += 1
    return copies
# Optional[t] --> Union[t, None, boolen] 
                             # Sequence[T]   
def search(needle: str, haystack: List[str]) -> Optional[int]:
def search(needle: str, haystack: List[str]) -> Union[int, None]:
    xxxxx
    return xxx

count(1, [1,2,3,4,5,1])
count("b", ["a", "b", "c"])
print


# modeling
# data modles/ methamatical models/ domain models/ data flow models
# as a communication tools-> to convey the fundamental principles and 
# basic funcionality of systems
# four communicating modles

1. understandability -> understand by human first
what it does not how it does


from itertools import combinations
MAGIC = [[4,9,2],[3,5,7],[8,1,6]]

def has15(numbers):
    """
    for n1 in numbers:
        for n2 in numbers:
            for n3 in numbers:
                if n1 != n2 != n3 and n1 + n2 + n3 == 15 
                    return True
    """
    for c in combinations(numbers, 3):
        if sum(c) == 15:
            return True                    
    return False          
                    
# extensibility obsession
# reusablity
class TicTacToc:
    def __init__(self):
        self.playerA = []
        self.playerO = []
    def value(self, row, col):
        n = MAGIC[row][col]
        if n in self.playerX:
            return 'x'
        elif n in self.playerO:
            return 'O'
        else:
            return None 
    def winner(self):
        if has15(self.playerA):
            return 'A'
        if has15(self.playerO)
            return 'O'
