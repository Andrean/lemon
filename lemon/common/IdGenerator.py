'''
Created on 14.06.2013

@author: vau
'''
import time
import random

random.seed()

def GenerateNewUniqueID():
    _id = str(int(time.time()) % 1677721) + str(random.randint(1000000,9999999));
    return _id;

def GenerateSessionID():
    _id = random.randint(1000000,9999999)
    _id = str(_id) + str(random.randint(1000000,9999999))
    _id = _id + str(random.randint(1000000,9999999)) 
    return _id