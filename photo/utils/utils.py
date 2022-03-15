import random


def code():
    a = ''
    for x in range(4):
        a += str(random.randint(0, 9))
    return a