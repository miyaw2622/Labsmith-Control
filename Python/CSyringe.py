import numpy as np
from datetime import datetime
import time

class CSyringe:

    def __init__(self, Lboard, add_syr):
        self.Lboard = Lboard
        self.add_syr = add_syr
        
        # General info
        self.device = []
        self.name = []
        self.address = []
        
        # Syringes info
        self.maxFlowrate = []
        self.minFlowrate = []
        self.Flowrate = []
        self.diameter = []
        self.maxVolume = []
        
        # Flags
        self.FlagIsMoving = False
        self.FlagIsDone = True
        self.FlagIsOnline = False
        self.FlagIsStalled = False
        self.FlagIsMovingIn = False
        self.FlagIsMovingOut = False
        self.FlagReady = True
        self.FlagStop = False
                
        # Clocks
        self.ClockStartCmd = None
        self.ClockStopCmd = None

        ### Constructor
        self.device = self. Lboard.eib.NewSPS01(np.int8(add_syr))
        self.name = self.device.GetName
        self.diameter = self.device.CmdGetDiameter()
        self.maxFlowrate = self.device.GetMaxFlowrate()
        self.minFlowrate = self.device.GetMinFlowrate()
        self.maxVolume = self.device.GetMaxVolume()
        
        self.addlistener('MovingState', 'listener', self.Updating(), []) #it listens for the self.FlagIsMoving == true, so it updtades continuously the state to determine the end of the command. self.Ready = true again.
        self.addlistener('FlagStop', 'listener_stop', self.StopSyr(), []) #it listens for the self.FlagIsMoving == true, so it updtades continuously the state to determine the end of the command. self.Ready = true again.
        
        self.UpdateStatus()
        
        with open("OUTPUT.txt", "a") as OUTPUT:
            comment = f"Syringe {self.name} loaded."
            OUTPUT.write(comment + "\n")
            print(comment)


        ## Events
        self._listeners = {event: dict() for event in ["MovingState"]}
        
        
    ## Add Listeners to Events
    def addlistener(self, event, listener, callback, args):
        if callable(callback):
            self._listeners[event][listener] = [callback, args]

    ## Trigger Events
    def notify(self, event):
        for listener, [callback, args] in self._listeners[event].items():
            callback(*args)

    ### UpdateStaus
    def UpdateStatus(self):
        self.device.CmdGetStatus()
        self.FlagIsDone = self.device.IsDone()
        self.FlagIsMoving = self.device.IsMoving()
        self.FlagIsOnline = self.device.IsOnline()
        self.FlagIsStalled = self.device.IsStalled()
        self.FlagIsMovingIn = self.device.IsMovingIn()
        self.FlagIsMovingOut = self.device.IsMovingOut()
        if self.FlagIsStalled == True:
            with open("OUTPUT.txt", "a") as OUTPUT:
                self.device.CmdStop()
                comment = f"ERROR: Syringe {self.name} is stalled."
                OUTPUT.write(comment + "\n")
                print(comment)

    ### MoveTo        
    def MoveTo(self,flowrate,volume):
        if self.FlagIsDone == True:
            self.device.CmdSetFlowrate(flowrate)
            self.Flowrate = flowrate
            self.device.CmdMoveToVolume(volume)
            self.FlagReady = False
            self.displaymovement()
            if self.FlagIsMoving == True:
                self.notify('MovingState')

    ### Display movement In and Out on cmdwindow              
    def displaymovement(self):
        self.ClockStartCmd = datetime.now()
        self.UpdateStatus(self)
        if self.FlagIsMovingIn == True:
            with open("OUTPUT.txt", "a") as OUTPUT:
                self.device.CmdStop()
                comment = f"{self.ClockStartCmd.strftime('%X')} Syringe {self.name} is pulling at {self.Flowrate} ul/min."
                OUTPUT.write(comment + "\n")
                print(comment)
        elif self.FlagIsMovingOut == True:
            with open("OUTPUT.txt", "a") as OUTPUT:
                self.device.CmdStop()
                comment = f"{self.ClockStartCmd.strftime('%X')} Syringe {self.name} is pushing at {self.Flowrate} ul/min."
                OUTPUT.write(comment + "\n")
                print(comment)
            
    ### Display stop movement on cmdwindow             
    def displaymovementstop(self):
        self.ClockStopCmd = datetime.now()
        with open("OUTPUT.txt", "a") as OUTPUT:
                self.device.CmdStop()
                comment = f"{self.ClockStartCmd.strftime('%X')} Syringe {self.name} is done."
                OUTPUT.write(comment + "\n")
                print(comment)
        self.FlagReady = True
    
    ### Listener function
    def Updating(self):
        if self.FlagIsMoving == True:
            while self.FlagIsMoving == True:
                self.UpdateStatus()
            if self.FlagIsDone == True:
                self.displaymovementstop()

    def StopSyr(self):
        if self.FlagStop == True:
            self.device.CmdStop()
            self.FlagStop = False

    ### Stop
    def Stop(self):
        self.device.CmdStop()
        self.UpdateStatus()
        self.FlagReady = True

    ### Wait
    def Wait(self,time_sec):
        time.sleep(time_sec)
        self.Stop()
