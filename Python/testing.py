class Main:
    def __init__(self):
        self._listeners = {event: dict() for event in ["event1"]}
        # self.other = Test()
        
    ## Add Listeners to Events
    def func(self, *args):
        print(len(args))




obj = Main()
obj.func(1, 2, 3)
