Example:

# TODO app
- As a user, I want to add a task so that I don't have to remember to do it
    -An add button should appear on the right- hand side
    -clicking button should present dialog with text box
    - user clicks confirm add the tast to the list
    - The user has an indicator of how to create  a task
    - The user can enter text to creat a task    
- As a user, I want to mask a task as done, such that I dont have to be reminded again


- As a user, I want to mark a task as done, such that I DONT have to reminded agian
- Scenario: Task has been completed
- Given: The suer has the task in a list in front of them
- when: The user ticks the done box
- then : the task is greyed out
- and: no longer appers in the list of pending tasks


# Fronted end  
http preview vscode  

# TESTING // property based testing
from hypothesis import given, strategies, Verbosity, settings

def bubblesort(numbers):
    numbers = number.copy()
    for i in range(len(numbers) - 1):
        for j in range(len(numbers) - 1):
            if numbers[j] > numbers[j+1]:
                numbers[i], numebrs[i+1] = numbers[i+1], numbers[i]
    return numbers
                
@given(strategies.lists(strategies.integers()))
@settings(verbosity=Verbosity.verbose)
def test_length(nums):
    assert len(bubblesort(nums)) == len(nums)
def test_idempotence(nums):
    assert bubblesort(nums) == bubblesort(bubblesort(nums))

def is_sorted(nums):
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return False
    return True
@given(strategies.lists(strategies.integers()))
def test_sorted(nums):
    assert is_sorted(bubblesort(nums))    

# use a set with count
def is_permutations(nums1,nums2):
    d1 = {}
    for n in nums1:
        if n in d1:
            d1[n] += 1
        else:
            d1[n] = 1
    d2 = {}
    for n in nums2:
        if n in d2:
            d2[n] += 1
        else:
            d2[n] = 1                      
    return d1 == d2

@given(strategies.lists(strategies.integers()))
def test_permutations(nums):
    assert is_permu(nums, bubblesort(nums))                            
    
