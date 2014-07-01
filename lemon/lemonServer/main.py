'''
Created on 13.06.2013

@author: vau
'''
import core
import time

if __name__ == '__main__':

    c = core.Core()
    core.setCoreInstance(c)
    c.start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        c.stop()