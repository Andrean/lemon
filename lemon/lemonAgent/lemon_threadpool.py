'''
Created on 14.08.2013

@author: vau
'''
import threading
import queue
import time

QUEUE_MAXSIZE   = 400

class ThreadPool(threading.Thread):
    def __init__(self, max_threads=15):
        self.max_threads    = max_threads
        self._last_free_thread   = 0
        self._threads   = []
        self._threadInfo    = []
        self._taskQueue = queue.Queue(QUEUE_MAXSIZE)
        threading.Thread.__init__(self)       
                
    def run(self):
        for i in range(0,self.max_threads):
            self._threadInfo.append({'s':0})
            self._threads.append(TaskThread(self._threadInfo[i]))                        
        self._running = True
        while self._running:
            self._process()
    
    def put(self, _task):
        self._taskQueue.put(_task)       
    
    def _process(self):
        try:            
            n   = self._getFreeThread()
            task    = self._taskQueue.get(True, 1)
            self._start_task(n, task)
        except queue.Empty:
            return
        except NoFreeThreads:
            self._logger.debug('No free threads in ThreadPool')
            time.sleep(1)
            return
        except:
            pass
                
    def _start_task(self, thread_num, task):
        self._threads[thread_num]   = TaskThread(self._threadInfo[thread_num])              
        self._threads[thread_num].assign(task)
        self._threads[thread_num].start() #### РАЗОБРАТЬСЯ!!!
    
    def _getFreeThread(self):
        i   = self.max_threads
        while i > 0:
            if self._threadInfo[self._last_free_thread]['s'] == 0:
                return self._last_free_thread
            else:
                self._last_free_thread = (self._last_free_thread + 1) % self.max_threads
            i -= 1
        raise NoFreeThreads                    
            
    
    def quit(self):
        self._running = False
    

class TaskThread(threading.Thread):
    def __init__(self, _info, task = None ):
        self._task    = task
        self._info    = _info
        threading.Thread.__init__(self)
    
    def run(self):        
        self._info['s'] = 1
        self._task.run()
        self._info['s'] = 0
        
    def assign(self,_task):
        self._task = _task

class NoFreeThreads(Exception):
    pass