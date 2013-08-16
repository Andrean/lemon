'''
Created on 14.08.2013

@author: vau
'''
import threading
import queue
import time

class ThreadPool(threading.Thread):
    def __init__(self, max_threads=5):
        self.max_threads    = max_threads
        self._threads   = []
        self._taskQueue = queue.Queue()
        threading.Thread.__init__(self)
       
                
    def run(self):
        for _ in range(0,self.max_threads-1):
            self._threads.append(TaskThread())
        self._running = True
        while self._running:
            self._process()
    
    def put(self, _task):
        self._taskQueue.put(_task)
    
    def _process(self):
        if self._taskQueue.empty() is True:
            time.sleep(0.05) 
        else:
            n   = self._getFreeThread()
            if n >= 0:
                task    = self._taskQueue.get()
                self._start_task(n, task)
                    
    def _start_task(self, thread_num, task):
        self._threads[thread_num].assign(task)
        self._threads[thread_num].run()
    
    def _getFreeThread(self):
        for i, t in enumerate(self._threads):
            if t.is_alive() is not True:
                return i;
        return -1;
    
    def quit(self):
        self._running = False
    

class TaskThread(threading.Thread):
    def __init__(self, task = None):
        self._task    = task
        threading.Thread.__init__(self)
    
    def run(self):
        self._task.run()
        
    def assign(self,_task):
        self._task = _task