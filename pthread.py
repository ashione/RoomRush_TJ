#!/usr/bin/python
import roomRush
import threading
import time
class Pthread(threading.Thread): 
    def __init__(self,roomRush ):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.threadRoom = roomRush
    def run(self): 
        while not self.thread_stop:
                    self.threadRoom.run()
    def stop(self):
        self.thread_stop = True
