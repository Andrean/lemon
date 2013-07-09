'''
Created on 09.07.2013
Task templates, which used to do some useful actions
@author: vau
'''

def runCounter(t, counter_id, kwargs):
    pass

def testPrint(t, kwargs):
    print(kwargs['los'])
    try:
        if kwargs['t']:
            print('i am task with id '+str(t.id))
    except KeyError:
        pass
        
CMD = {}
CMD['runCounter']   = runCounter
CMD['testPrint']    = testPrint
