#!/usr/bin/python
import random
import sys

def some_instructions(min, max):
    result = list()
    
    n = random.randint(min, max)
    
    for i in range(0, n):
        nn = random.randint(0, 5)
        
        if nn == 0:
            result.append('FORW ' + str(random.randint(1,100)) + '.')
        if nn == 1:
            result.append('BACK ' + str(random.randint(1,100)) + '.')
        if nn == 2:
            result.append('LEFT ' + str(random.randint(1,100)) + '.')
        if nn == 3:
            result.append('RIGHT ' + str(random.randint(1,100)) + '.')
        if nn == 4:
            result.append('UP.')
        if nn == 5:
            result.append('DOWN.')
    
    return result

def insert_reps(stuff, num):
    for i in range(0, num):
        start = random.randint(0, len(stuff) - 1)
        stop = random.randint(start, len(stuff) - 1)
        
        stuff[start] = 'REP ' + str(random.randint(1, 50)) + ' "' + stuff[start]
        stuff[stop] = stuff[stop] + '"'
    
    return stuff

program = some_instructions(int(sys.argv[1]), int(sys.argv[1]))
program = insert_reps(program, int(sys.argv[2]))
print("\n".join(program))
