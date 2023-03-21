#!/usr/bin/etc python
              
class StateMachine:
    
    def __init__(self):
        self.handlers = {}
        self.startState = None

    def add_state(self, name, handler):
        name = name.upper()
        self.handlers[name] = handler

    def set_start(self, name):
        self.startState = name.upper()

    def run(self):        
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
     
        while True:
            newState = handler()
            if newState == 'EXIT':
                break
            handler = self.handlers[newState.upper()]

