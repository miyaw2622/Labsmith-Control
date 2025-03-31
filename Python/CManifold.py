import numpy as np
from datetime import datetime

class CManifold:

    def __init__(self, Lboard, add_syr):
        
        self.Lboard = Lboard
        self.add_syr = add_syr
        
        # General info
        self.device = []
        self.name = []
        self.address = []
        
        # Flags
        # self.FlagIsMoving = False
        self.FlagIsDone = True
        self.FlagIsOnline = False
        self.FlagReady = True
        
        # Clocks
        self.ClockStartCmd = None
        self.ClockStopCmd = None

        ### Constructor
        self.device = self.Lboard.eib.New4VM(np.int8(self.add_syr))
        self.name= self.device.GetName()
        
        self.UpdateStatus()

        with open("OUTPUT.txt", "a") as OUTPUT:
            comment = f"Manifold {self.name} loaded."
            OUTPUT.write(comment + "\n")
            print(comment)

    ### UpdateStaus
    def UpdateStatus(self):
        self.device.CmdGetStatus()
        self.FlagIsDone = self.device.IsDone()
        self.FlagIsOnline = self.device.IsOnline()

    ### Switch Valves
    def SwitchValves(self,v1,v2,v3,v4):
            self.device.CmdSetValves(np.int8(v1),np.int8(v2),np.int8(v3),np.int8(v4))
            self.FlagReady = False
            self.displayswitch(v1,v2,v3,v4)
            while self.FlagIsDone == False:
                self.UpdateStatus()
            if self.FlagIsDone == True:
                self.displayswitchstop()

    ### Display switch start
    def displayswitch(self,v1,v2,v3,v4):
        self.ClockStartCmd = datetime.now()
        self.UpdateStatus()
        with open("OUTPUT.txt", "a") as OUTPUT:
            comment = f"{self.ClockStartCmd.strftime('%X')} 4VM {self.name} is switching valves to {v1}, {v2}, {v3}, {v4}."
            OUTPUT.write(comment + "\n")
            print(comment)

    ### Display switch stop
    def displayswitchstop(self):
        self.ClockStopCmd = datetime.now()
        # self.UpdateStatus()
        with open("OUTPUT.txt", "a") as OUTPUT:
            comment = f"{self.ClockStopCmd.strftime('%X')} 4VM {self.name} is done."
            OUTPUT.write(comment + "\n")
            print(comment)
        self.FlagReady = True

