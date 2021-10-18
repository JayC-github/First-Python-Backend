'''
Cycle finding exercise
'''

def longest_distance(elements):
    '''
    Find the length of the longest distance between two equal elements in the
    given list.
    For example:
    >>> longest_distance([1,2,3,1,4])
    3

    Params:
      input (list): A list of hashable elements.

    Returns:
      int: The length of the longest distance. Note, this could be zero.
    '''
    data = {}
    maxDis = 0
    # find the equal element and their distance
    for i in range(len(elements)):
        # if element not in the dic, insert the index of element
        if elements[i] not in data:
            data[elements[i]] = i
        # if element already in the dic, find their distance
        else:
            maxDis = max(maxDis, i - data[elements[i]])
    
    
    return maxDis

def test_documentation():
    '''
    Test from documentation
    '''
    assert longest_distance([1,2,3,1,4]) == 3

def test_starts_later():
    '''
    The longest distance doesn't include the first element in the list
    '''
    assert longest_distance([1,2,3,4,2,5]) == 3

def test_two_non_zero_distances():
    '''
    The distance between 2 and 2 is longest so its length is returned
    '''
    assert longest_distance([1,2,1,3,4,2]) == 4

def test_unique():
    '''
    All elements are unique, so the only distances are between the elements and
    themselves
    '''
    assert longest_distance([1,2,3,4]) == 0

def test_all_same():
    """
    All elements are the same, check if return the longest distance
    """ 
    
    assert longest_distance([1,1,1,1,1]) == 4
