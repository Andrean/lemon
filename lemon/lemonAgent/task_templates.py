'''
Created on 09.07.2013
Task templates, which used to do some useful actions
@author: vau
'''

def runCounter(t, counter_id, kwargs):
    pass

def addScheduledTask(t, kwargs):
    func_name       = kwargs['func']
    schtask_name    = kwargs['name']
    start_time      = kwargs['start_time']
    interval        = kwargs['interval']
    func_kwargs     = kwargs['kwargs']
    scheduler       = t._parent.scheduler
    scheduler.add(func_name, schtask_name, start_time, interval, func_kwargs)
    
def getNewData(t, kwargs):
    i           = t._parent.interfaceInstance
    new_data    = i.get('new')
    for k in new_data:
        print(i.get(k))
    
def refresh(t, kwargs):
    i           = t._parent.interfaceInstance
    result  = i.get()    
    
def testPrint(t, kwargs):
    print(kwargs['los'])
    try:
        if kwargs['t']:
            print('i am task with id '+str(t.id))
    except KeyError:
        pass
    

        
CMD = {}
CMD['runCounter']           = runCounter
CMD['testPrint']            = testPrint
CMD['addScheduledTask']     = addScheduledTask
CMD['getNewData']           = getNewData
CMD['refresh']              = refresh
