def shout(string):
    return string.upper() + "!!!!"
    
if __name__ == '__main__':
    tutors = ['Jay', 'Mercy', 'tom']
    angry_tutors = list(map(shout, tutors))
    #angry_tutors = list(map(lambda t: t.upper() + "!!!!", tutors)) 
    print(angry_tutors)
    print(tutors)    
