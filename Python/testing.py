# class Test:
#     def __init__(self):
#         self._listeners = {event: dict() for event in ["event1"]}
        
#     ## Add Listeners to Events
#     def addlistener(self, event, listener, callback):
#         if callable(callback):
#             self._listeners[event][listener] = callback

#     ## Trigger Events
#     def notify(self, event):
#         for listener, callback in self._listeners[event].items():
#             callback

#     def func(self, num):
#         self.addlistener('event1', "listener_1", self.listenerfunc(num))
        
#     def listenerfunc(self, num):
#         print("other number", num)

#     def trigger_event(self):
#         self.notify('event1')

class Main:
    def __init__(self):
        self._listeners = {event: dict() for event in ["event1"]}
        # self.other = Test()
        
    ## Add Listeners to Events
    def addlistener(self, event, listener, callback, args):
        if callable(callback):
            self._listeners[event][listener] = [callback, args]

    ## Trigger Events
    def notify(self, event):
        for listener, [callback, args] in self._listeners[event].items():
            callback(*args)

    def func(self, num1):
        # self.other.func(7)
        self.addlistener('event1', "listener_1", self.listenerfunc, [num1])
        
    def listenerfunc(self, num1):
        print("number", num1)

    def trigger_event(self):
        self.notify('event1')
        # self.other.notify('event1') 




obj = Main()
obj.func(5)
print(obj._listeners)
# print(obj.other._listeners)
obj.trigger_event()
