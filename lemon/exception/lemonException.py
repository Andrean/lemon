'''
Created on 18.06.2013

@author: vau
'''

class LemonException(Exception):
    '''
    project class extends native python class Exception
    using for throw and catch specific lemon project exceptions
    '''


    def __init__(self, message):
        '''
        Constructor
        '''
        pass
        

class StorageNotCreatedException(LemonException):
    '''
    Using for raise exception if storage class has not created
    '''

    def __init__(self, message):
        pass

class ServerExitException(LemonException):
    pass

class HandlerAlreadyInListException(LemonException):
    pass