import numpy as np
import time
from uProcess_x64 import uProcess_x64
from datetime import datetime
import shutil


class LabsmithBoard:    
    
    def __init__(self, port): # # com is the comment i show on the Output text area in the app
        ## General info
        self.MaxNumDev = []
        self.TotNumDev = [] 
        self.eib = [] 
        self.C4VM = [] 
        self.SPS01 = [] 

        self.eib=uProcess_x64.CEIB()
        self.port = port

        ## Flags
        self.isConnected = False 
        self.isDisconnected = True 
        self.Stop = False 
        self.Pause = False 
        self.Resume = False 
        self.flag_break_countpause = 0 
        self.flag_break_stop = 0 
        self.flag_a = 0   # # flag used in listener of MoveWait function used to print just the initial target waiting time
        self.flag_b = 0   # # flag used in listener of MoveWait function used to print just the initial target waiting time
                   
        ## Clocks
        self.ClockStartConnection = None
        self.ClockStopConnection = None
        self.ClockStop = None
        self.ClockResume = None
        
        
        ## Events
        self._listeners = {event: dict() for event in [
            "FirstDone",
            "FirstDoneStop",
            "FirstDoneStopM",
            "FirstDoneStopPause",
            "FirstDoneStopPauseM",
            "FirstDoneStopPauseWait"]}#
        

    ## Add Listeners to Events
    def addlistener(self, event, listener, callback, args):
        if callable(callback):
            self._listeners[event][listener] = [callback, args]

    ## Trigger Events
    def notify(self, event):
        for listener, [callback, args] in self._listeners[event].items():
            callback(*args)

    ### Constructor
    def Constructor(self):
        a=self.eib.InitConnection(np.int8(self.port))
        with open("OUTPUT.txt", "a") as OUTPUT:
            if a == 0:
                self.isConnected = True
                self.isDisconnected = False
                self.ClockStartConnection = datetime.now()
                comment=f"Connected on {self.ClockStartConnection}"
                self.Load()
            else:
                comment='Not connected, check the right COM port on Device Manager'
        
        OUTPUT.write(comment + "\n")
        print(comment)


    ### Destructor
    def Disconnect(self):
        a=np.int64(self.eib.CloseConnection())
        with open("OUTPUT.txt", "a") as OUTPUT:
            if a == 0:
                self.isConnected = False
                self.isDisconnected = True
                self.ClockStopConnection = datetime.now()
                com= f"Disconnected on {self.ClockStartConnection}"
                namefile=f"OUTPUT_{self.ClockStartConnection.strftime("%y_%m_%d_%H_%M_%S")}.txt"
                shutil.copy('OUTPUT.txt', namefile)
            else:
                com='Error, still connected'

        OUTPUT.write(com + "\n")
        print(com)
        return com
        
    ### Load
    def Load(self):
        dev_list=str(self.eib.CmdCreateDeviceList())
        expression = '\,'; ##i first split the string into multiple strings
        splitStr = dev_list.split(expression)##divide all the different devices. It is a cell array. Each cell is a segment of the dev_list char vector containing info about each device
        NumDev=len(splitStr)
        self.TotNumDev=NumDev

        PAT_S=" <uProcess.CSyringe>"
        PAT_M=" <uProcess.C4VM>"

        StrSyringe= [syringe for syringe in splitStr if PAT_S in syringe]
        StrManifold= [manifold for manifold in splitStr if PAT_M in manifold]

        if StrManifold:
            PAT="address " + d0igitsPattern
            add_man=extract(StrManifold,PAT); ##add_man ={'address 35'}{'address 74'} 2×1 cell array
            PAT=digitsPattern;
            add_man=str2double(extract(add_man,PAT)); ## OUTPUT 2: add_man =[35;74]. It is 2x1 vector containg the addresses of the manifolds on the board 
            self.C4VM=cell(1,length(add_man));
            for i=1:length(add_man)
                self.C4VM{1,i} = CManifold(self,add_man(i)); ## it constructs a SPS01 selfect on the specified address. We will use this for the command
                self.C4VM{1,i}.address=add_man(i);
            end
        end

        if ~isempty(StrSyringe)
            PAT="address " + digitsPattern;
            add_syr=extract(StrSyringe,PAT); ## add_syr = 5×1 cell array {'address 1' }{'address 3' }{'address 8' }{'address 14'}{'address 26'}
            PAT=digitsPattern;
            add_syr=str2double(extract(add_syr,PAT));## OUTPUT 4: add_syr =[1;3;8;14;26].  It is 5x1 vector containg the addresses of the syringes on the board                                
            self.SPS01=cell(1,length(add_syr));
            for i=1:length(add_syr)
                self.SPS01{1,i} = CSyringe(self,add_syr(i)); ## it constructs a SPS01 selfect on the specified address. We will use this for the command
                self.SPS01{1,i}.address=add_syr(i);

    ## TODO ##

    ### Stop
    def StopBoard(sefl):
        pass
    ## TODO ##
    
    ### Move
    def Move(self, namedevice, flowrate, volume):
        pass
    ## TODO ##
    
    ### Move2
    def Move2(self, namedevice, flowrate, volume):
        pass
    ## TODO ##
    
    ### FindIndexS (find index of Syringe from name of device)
    def FindIndexS(self, n):
        pass
    ## TODO ##
    
    ### FindIndexM (find index of Manifold from name of device)
    def FindIndexM(self, n):
        return [out, com]
    ## TODO ##

    ### Set Multiple FlowRates (at the same time)
    def SetFlowRate(self, d1,f1,d2,f2,d3,f3,d4,f4,d5,f5,d6,f6,d7,f7,d8,f8):
        pass
    ## TODO ##

    ### Multiple Movement (at the same time)
    def MulMove(self, d1 = None, v1 = None, d2  = None, v2 = None, d3 = None, v3 = None, d4 = None, v4 = None, d5 = None, v5 = None, d6 = None, v6 = None, d7 = None, v7 = None, d8 = None, v8 = None):
        if [d1, v1, d2, v2, d3, v3, d4, v4, d5, v5, d6, v6, d7, v7, d8, v8].count(None)%2 !=0:
            print('Error, missing input. Number of inputs has to be odd (interface, name of syringes and corresponding flow rates).')
        else:
            if d1 != None and v1 != None:  # # 1 syringe as input
                i1=self.FindIndexS(d1) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1])   # #it listens for the syringe FlagIsMoving == True, so it updtades continuously the state to determine the end of the command. It results in FlagReady = True again.
                if len(i1)>0:
                    if self.SPS01[0,i1].FlagIsDone == True:
                        self.SPS01[0,i1].device.CmdMoveToVolume(v1)                             
                        self.SPS01[0,i1].FlagReady = False 
                        self.SPS01[0,i1].displaymovement()
                        if self.SPS01[0,i1].FlagIsMoving == True:
                            self.SPS01[0,i1].notify('MovingState') 
            elif v2 != None and d3 == None:  # # 2 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2)  
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0:
                    if self.SPS01[0,i1].FlagIsDone == True and self.SPS01[0,i2].FlagIsDone == True:
                        self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                        self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                        self.SPS01[0,i1].FlagReady = False 
                        self.SPS01[0,i2].FlagReady = False 
                        self.SPS01[0,i1].displaymovement()
                        self.SPS01[0,i2].displaymovement()  
                        if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True:
                            self.notify('FirstDone') 

            elif v3 != None and d4 == None:  # # 3 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2) 
                i3=self.FindIndexS(d3) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2,i3])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0:
                    self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[0,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[0,i1].FlagReady = False 
                    self.SPS01[0,i2].FlagReady = False 
                    self.SPS01[0,i3].FlagReady = False 
                    self.SPS01[0,i1].displaymovement()
                    self.SPS01[0,i2].displaymovement() 
                    self.SPS01[0,i3].displaymovement()
                    if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True:
                        self.notify('FirstDone')               
            elif v4 != None and d5 == None:  # # 4 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2) 
                i3=self.FindIndexS(d3) 
                i4=self.FindIndexS(d4) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2,i3,i4])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0:
                    self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[0,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[0,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[0,i1].FlagReady = False 
                    self.SPS01[0,i2].FlagReady = False 
                    self.SPS01[0,i3].FlagReady = False 
                    self.SPS01[0,i4].FlagReady = False 
                    self.SPS01[0,i1].displaymovement()
                    self.SPS01[0,i2].displaymovement() 
                    self.SPS01[0,i3].displaymovement()
                    self.SPS01[0,i4].displaymovement()
                    if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True:
                        self.notify('FirstDone') 
            elif v5 != None and d6 == None:  # # 5 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2) 
                i3=self.FindIndexS(d3) 
                i4=self.FindIndexS(d4) 
                i5=self.FindIndexS(d5) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2,i3,i4,i5])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0:
                    self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[0,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[0,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[0,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[0,i1].FlagReady = False 
                    self.SPS01[0,i2].FlagReady = False 
                    self.SPS01[0,i3].FlagReady = False 
                    self.SPS01[0,i4].FlagReady = False 
                    self.SPS01[0,i5].FlagReady = False 
                    self.SPS01[0,i1].displaymovement()
                    self.SPS01[0,i2].displaymovement() 
                    self.SPS01[0,i3].displaymovement()
                    self.SPS01[0,i4].displaymovement()
                    self.SPS01[0,i5].displaymovement()
                    if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True:
                        self.notify('FirstDone') 
            elif v6 != None and d7 == None:  # # 6 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2) 
                i3=self.FindIndexS(d3) 
                i4=self.FindIndexS(d4) 
                i5=self.FindIndexS(d5) 
                i6=self.FindIndexS(d6) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2,i3,i4,i5,i6])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0 and len(i6)>0:
                    self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[0,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[0,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[0,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[0,i6].device.CmdMoveToVolume(v6) 
                    self.SPS01[0,i1].FlagReady = False 
                    self.SPS01[0,i2].FlagReady = False 
                    self.SPS01[0,i3].FlagReady = False 
                    self.SPS01[0,i4].FlagReady = False 
                    self.SPS01[0,i5].FlagReady = False 
                    self.SPS01[0,i6].FlagReady = False 
                    self.SPS01[0,i1].displaymovement()
                    self.SPS01[0,i2].displaymovement() 
                    self.SPS01[0,i3].displaymovement()
                    self.SPS01[0,i4].displaymovement()
                    self.SPS01[0,i5].displaymovement()
                    self.SPS01[0,i6].displaymovement()
                    if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True:
                        self.notify('FirstDone') 
            elif v7 != None and d8 == None:  # # 7 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2) 
                i3=self.FindIndexS(d3) 
                i4=self.FindIndexS(d4) 
                i5=self.FindIndexS(d5) 
                i6=self.FindIndexS(d6) 
                i7=self.FindIndexS(d7) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2,i3,i4,i5,i6,i7])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0 and len(i6)>0 and len(i7)>0:
                    self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[0,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[0,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[0,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[0,i6].device.CmdMoveToVolume(v6) 
                    self.SPS01[0,i7].device.CmdMoveToVolume(v7) 
                    self.SPS01[0,i1].FlagReady = False 
                    self.SPS01[0,i2].FlagReady = False 
                    self.SPS01[0,i3].FlagReady = False 
                    self.SPS01[0,i4].FlagReady = False 
                    self.SPS01[0,i5].FlagReady = False 
                    self.SPS01[0,i6].FlagReady = False 
                    self.SPS01[0,i7].FlagReady = False 
                    self.SPS01[0,i1].displaymovement()
                    self.SPS01[0,i2].displaymovement() 
                    self.SPS01[0,i3].displaymovement()
                    self.SPS01[0,i4].displaymovement()
                    self.SPS01[0,i5].displaymovement()
                    self.SPS01[0,i6].displaymovement()
                    self.SPS01[0,i7].displaymovement()
                    if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True:
                        self.notify('FirstDone') 
            elif v8 != None:  # # 8 syringes as input
                i1=self.FindIndexS(d1) 
                i2=self.FindIndexS(d2) 
                i3=self.FindIndexS(d3) 
                i4=self.FindIndexS(d4) 
                i5=self.FindIndexS(d5) 
                i6=self.FindIndexS(d6) 
                i7=self.FindIndexS(d7) 
                i8=self.FindIndexS(d8) 
                self.addlistener('FirstDone', "listener_firstdone", self.CheckFirstDone, [i1,i2,i3,i4,i5,i6,i7,i8])   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0 and len(i6)>0 and len(i7)>0 and len(i8)>0:
                    self.SPS01[0,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[0,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[0,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[0,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[0,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[0,i6].device.CmdMoveToVolume(v6) 
                    self.SPS01[0,i7].device.CmdMoveToVolume(v7) 
                    self.SPS01[0,i8].device.CmdMoveToVolume(v8) 
                    self.SPS01[0,i1].FlagReady = False 
                    self.SPS01[0,i2].FlagReady = False 
                    self.SPS01[0,i3].FlagReady = False 
                    self.SPS01[0,i4].FlagReady = False 
                    self.SPS01[0,i5].FlagReady = False 
                    self.SPS01[0,i6].FlagReady = False 
                    self.SPS01[0,i7].FlagReady = False 
                    self.SPS01[0,i8].FlagReady = False 
                    self.SPS01[0,i1].displaymovement()
                    self.SPS01[0,i2].displaymovement() 
                    self.SPS01[0,i3].displaymovement()
                    self.SPS01[0,i4].displaymovement()
                    self.SPS01[0,i5].displaymovement()
                    self.SPS01[0,i6].displaymovement()
                    self.SPS01[0,i7].displaymovement()
                    self.SPS01[0,i8].displaymovement()
                    if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True and self.SPS01[0,i8].FlagIsMoving == True:
                        self.notify('FirstDone')
            else:
                print('Error, missing input. Number of inputs has to be odd (interface, name of syringes and corresponding flow rates).')

    ## Multiple Movement with stop (at the same time. It allows the stop)
    def MulMove2(self,d1,v1,d2,v2,d3,v3,d4,v4,d5,v5,d6,v6,d7,v7,d8,v8):
        pass
    ## TODO ##

    ### Listener Function : Display the first device to be done (called in MulMove)
    def CheckFirstDone(self, *args):
        if len(args) == 4:  # # only one syringe in motion (=numb input + self + 2more input (source and event))   
            i1=args[2]   # #argsg doesnt include the self, so its size is len(args)-1. The index is the last.
            if self.SPS01[0,i1].FlagIsMoving == True:
                while self.SPS01[0,i1].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True:
                    self.SPS01[0,i1].displaymovementstop()
        elif len(args) == 5:
            i1=args[2]  
            i2=args[3] 
            i=[i1, i2]  
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True :
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus()
                    self.SPS01[0,i2].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i[j]].FlagIsDone == True:
                            self.SPS01[0, i[j]].displaymovementstop()
                            a=i 
                            a(j)=[]   # # a=[i2] for j=1, a=[i1] for j=2
                            while self.SPS01[0,a[0]].FlagIsMoving == True:
                                self.SPS01[0,a[0]].UpdateStatus()                            
                            if self.SPS01[0,a[0]].FlagIsDone == True:
                                self.SPS01[0,a[0]].displaymovementstop()                               
                            break
        elif len(args) == 6:
            i1=args[2]  
            i2=args[3] 
            i3=args[4] 
            i=[i1, i2, i3]  
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True: 
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus() 
                    self.SPS01[0,i2].UpdateStatus() 
                    self.SPS01[0,i3].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i[j]].FlagIsDone == True:
                            self.SPS01[0,i[j]].displaymovementstop()
                            a=i 
                            a[j]=[]   # # a=[i2 i3] for j=1, a=[i1 i3] for j=2, a=[i1 i2] for j=3
                            while self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True:
                                    self.SPS01[0,a[0]].UpdateStatus() 
                                    self.SPS01[0,a[1]].UpdateStatus()
                            if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True:
                                for k in range(len(a[0])):
                                    if self.SPS01[0,a[k]].FlagIsDone == True:
                                        self.SPS01[0,a[k]].displaymovementstop()
                                        b=a 
                                        b[k]=[] 
                                        while self.SPS01[0,b[0]].FlagIsMoving == True:
                                            self.SPS01[0,b[0]].UpdateStatus()                                  
                                        if self.SPS01[0,b(1)].FlagIsDone == True:
                                            self.SPS01[0,b[0]].displaymovementstop()                     
                                        break
                            break
        elif len(args) == 7:
            i1=args[2]  
            i2=args[3] 
            i3=args[4] 
            i4=args[5] 
            i=[i1, i2, i3, i4]  
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True:
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus() 
                    self.SPS01[0,i2].UpdateStatus() 
                    self.SPS01[0,i3].UpdateStatus() 
                    self.SPS01[0,i4].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i[j]].FlagIsDone == True:
                            self.SPS01[0,i[j]].displaymovementstop()
                            a=i 
                            a[j]=[]  
                            while self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True:
                                    self.SPS01[0,a[0]].UpdateStatus() 
                                    self.SPS01[0,a[1]].UpdateStatus() 
                                    self.SPS01[0,a[2]].UpdateStatus()
                            if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True:
                                for k in range(len(a[0])):
                                    if self.SPS01[0,a[k]].FlagIsDone == True:
                                        self.SPS01[0,a[k]].displaymovementstop()
                                        b=a 
                                        b[k]=[] 
                                        while self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True:
                                            self.SPS01[0,b[0]].UpdateStatus() 
                                            self.SPS01[0,b[1]].UpdateStatus()
                                        if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True:
                                            for p in range(len(b[0])):
                                                if self.SPS01[0,b[p]].FlagIsDone == True:
                                                    self.SPS01[0,b[p]].displaymovementstop()
                                                    c=b 
                                                    c[p]=[] 
                                                    while self.SPS01[0,c[0]].FlagIsMoving == True:
                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                    if self.SPS01[0,c[0]].FlagIsDone == True:
                                                        self.SPS01[0,c[0]].displaymovementstop()
                                                    break
                                        break
                            break
        elif len(args) == 8:
            i1=args[2]  
            i2=args[3] 
            i3=args[4] 
            i4=args[5] 
            i5=args[6] 
            i=[i1, i2, i3, i4, i5]  
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True:
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus() 
                    self.SPS01[0,i2].UpdateStatus() 
                    self.SPS01[0,i3].UpdateStatus() 
                    self.SPS01[0,i4].UpdateStatus() 
                    self.SPS01[0,i5].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i[j]].FlagIsDone == True:
                            self.SPS01[0,i[j]].displaymovementstop()
                            a=i 
                            a[j]=[]  
                            while self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True:
                                    self.SPS01[0,a[0]].UpdateStatus()
                                    self.SPS01[0,a[1]].UpdateStatus()
                                    self.SPS01[0,a[2]].UpdateStatus()
                                    self.SPS01[0,a[3]].UpdateStatus()
                            if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True:
                                for k in range(len(a[0])):
                                    if self.SPS01[0,a[k]].FlagIsDone == True:
                                        self.SPS01[0,a[k]].displaymovementstop()
                                        b=a 
                                        b[k]=[] 
                                        while self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True:
                                            self.SPS01[0,b[0]].UpdateStatus()
                                            self.SPS01[0,b[1]].UpdateStatus()
                                            self.SPS01[0,b[2]].UpdateStatus()
                                        if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True:
                                            for p in range(len(b[0])):
                                                if self.SPS01[0,b[p]].FlagIsDone == True:
                                                    self.SPS01[0,b[p]].displaymovementstop()
                                                    c=b 
                                                    c[p]=[] 
                                                    while self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving:
                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                        self.SPS01[0,c[1]].UpdateStatus()
                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True:
                                                        for q in range(len(c[0])):
                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                d=c 
                                                                d[q]=[] 
                                                                while self.SPS01[0,d[0]].FlagIsMoving:
                                                                    self.SPS01[0,d[0]].UpdateStatus()
                                                                if self.SPS01[0,d[0]].FlagIsDone:
                                                                    self.SPS01[0,d[0]].displaymovementstop()
                                                                break
                                                    break
                                        break
                            break
        elif len(args) == 9:
            i1=args[2]  
            i2=args[3] 
            i3=args[4] 
            i4=args[5] 
            i5=args[6] 
            i6=args[7] 
            i=[i1, i2, i3, i4, i5, i6]  
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True:
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus() 
                    self.SPS01[0,i2].UpdateStatus() 
                    self.SPS01[0,i3].UpdateStatus() 
                    self.SPS01[0,i4].UpdateStatus() 
                    self.SPS01[0,i5].UpdateStatus() 
                    self.SPS01[0,i6].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True or self.SPS01[0,i6].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i[j]].FlagIsDone == True:
                            self.SPS01[0,i[j]].displaymovementstop()
                            a=i
                            a[j]=[]
                            while self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True and self.SPS01[0,a[4]].FlagIsMoving == True:
                                    self.SPS01[0,a[0]].UpdateStatus()
                                    self.SPS01[0,a[1]].UpdateStatus()
                                    self.SPS01[0,a[2]].UpdateStatus()
                                    self.SPS01[0,a[3]].UpdateStatus()
                                    self.SPS01[0,a[4]].UpdateStatus()
                            if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True or self.SPS01[0,a[4]].FlagIsDone == True:
                                for k in range(len(a[0])):
                                    if self.SPS01[0,a[k]].FlagIsDone == True:
                                        self.SPS01[0,a[k]].displaymovementstop()
                                        b=a 
                                        b[k]=[] 
                                        while self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True and self.SPS01[0,b[3]].FlagIsMoving == True:
                                            self.SPS01[0,b[0]].UpdateStatus()
                                            self.SPS01[0,b[1]].UpdateStatus()
                                            self.SPS01[0,b[2]].UpdateStatus()
                                            self.SPS01[0,b[3]].UpdateStatus()
                                        if self.SPS01[0,b[[0]]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True or self.SPS01[0,b[3]].FlagIsDone == True:
                                            for p in range(len(b[0])):
                                                if self.SPS01[0,b[p]].FlagIsDone == True:
                                                    self.SPS01[0,b[p]].displaymovementstop()
                                                    c=b 
                                                    c[p]=[] 
                                                    while self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving and self.SPS01[0,c[2]].FlagIsMoving:
                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                        self.SPS01[0,c[1]].UpdateStatus()
                                                        self.SPS01[0,c[2]].UpdateStatus()
                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True or self.SPS01[0,c[2]].FlagIsDone == True:
                                                        for q in range(len(c[0])):
                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                d=c 
                                                                d[q]=[] 
                                                                while self.SPS01[0,d[0]].FlagIsMoving and self.SPS01[0,d[1]].FlagIsMoving:
                                                                    self.SPS01[0,d[0]].UpdateStatus()
                                                                    self.SPS01[0,d[1]].UpdateStatus()
                                                                if self.SPS01[0,d[0]].FlagIsDone or self.SPS01[0,d[1]].FlagIsDone:
                                                                    for r in range(len(d[0])):
                                                                        if self.SPS01[0,d[r]].FlagIsDone == True:
                                                                            self.SPS01[0,d[r]].displaymovementstop()
                                                                            e=d
                                                                            e[r]=[]
                                                                            while self.SPS01[0,e[0]].FlagIsMoving:
                                                                                self.SPS01[0,e[0]].UpdateStatus()
                                                                            if self.SPS01[0,e[0]].FlagIsDone:
                                                                                self.SPS01[0,e[1]].displaymovementstop()
                                                                            break
                                                                break
                                                    break
                                        break
                            break
        elif len(args) == 10:
            i1=args[2]  
            i2=args[3] 
            i3=args[4] 
            i4=args[5] 
            i5=args[6] 
            i6=args[7] 
            i7=args[8] 
            i=[i1, i2, i3, i4, i5, i6, i7]  
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True:
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus() 
                    self.SPS01[0,i2].UpdateStatus() 
                    self.SPS01[0,i3].UpdateStatus() 
                    self.SPS01[0,i4].UpdateStatus() 
                    self.SPS01[0,i5].UpdateStatus() 
                    self.SPS01[0,i6].UpdateStatus() 
                    self.SPS01[0,i7].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True or self.SPS01[0,i6].FlagIsDone == True or self.SPS01[0,i7].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i[j]].FlagIsDone == True:
                            self.SPS01[0,i[j]].displaymovementstop()
                            a=i 
                            a[j]=[]  
                            while self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True and self.SPS01[0,a[4]].FlagIsMoving == True and self.SPS01[0,a[5]].FlagIsMoving == True:
                                    self.SPS01[0,a[0]].UpdateStatus() 
                                    self.SPS01[0,a[1]].UpdateStatus() 
                                    self.SPS01[0,a[2]].UpdateStatus() 
                                    self.SPS01[0,a[3]].UpdateStatus() 
                                    self.SPS01[0,a[4]].UpdateStatus() 
                                    self.SPS01[0,a[5]].UpdateStatus()
                            if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True or self.SPS01[0,a[4]].FlagIsDone == True or self.SPS01[0,a[5]].FlagIsDone == True:
                                for k in range(len(a[0])):
                                    if self.SPS01[0,a[k]].FlagIsDone == True:
                                        self.SPS01[0,a[k]].displaymovementstop()
                                        b=a 
                                        b[k]=[] 
                                        while self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True and self.SPS01[0,b[3]].FlagIsMoving == True and self.SPS01[0,b[4]].FlagIsMoving == True:
                                            self.SPS01[0,b[0]].UpdateStatus() 
                                            self.SPS01[0,b[1]].UpdateStatus() 
                                            self.SPS01[0,b[2]].UpdateStatus() 
                                            self.SPS01[0,b[3]].UpdateStatus() 
                                            self.SPS01[0,b[4]].UpdateStatus()
                                        if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True or self.SPS01[0,b[3]].FlagIsDone == True or self.SPS01[0,b[4]].FlagIsDone == True:
                                            for p in range(len(b[0])):
                                                if self.SPS01[0,b[p]].FlagIsDone == True:
                                                    self.SPS01[0,b[p]].displaymovementstop()
                                                    c=b 
                                                    c[p]=[] 
                                                    while self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving and self.SPS01[0,c[2]].FlagIsMoving and self.SPS01[0,c[3]].FlagIsMoving:
                                                        self.SPS01[0,c[0]].UpdateStatus() 
                                                        self.SPS01[0,c[1]].UpdateStatus() 
                                                        self.SPS01[0,c[2]].UpdateStatus() 
                                                        self.SPS01[0,c[3]].UpdateStatus()
                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True or self.SPS01[0,c[2]].FlagIsDone == True or self.SPS01[0,c[3]].FlagIsDone == True:
                                                        for q in range(len(c[0])):
                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                d=c 
                                                                d[q]=[] 
                                                                while self.SPS01[0,d[0]].FlagIsMoving and self.SPS01[0,d[1]].FlagIsMoving and self.SPS01[0,d[2]].FlagIsMoving:
                                                                    self.SPS01[0,d[0]].UpdateStatus() 
                                                                    self.SPS01[0,d[1]].UpdateStatus() 
                                                                    self.SPS01[0,d[2]].UpdateStatus()
                                                                if self.SPS01[0,d[0]].FlagIsDone or self.SPS01[0,d[1]].FlagIsDone or self.SPS01[0,d[2]].FlagIsDone:
                                                                    for r in range(len(d[0])):
                                                                        if self.SPS01[0,d[r]].FlagIsDone == True:
                                                                            self.SPS01[0,d[r]].displaymovementstop()
                                                                            e=d 
                                                                            e[r]=[] 
                                                                            while self.SPS01[0,e[0]].FlagIsMoving and self.SPS01[0,e[1]].FlagIsMoving:
                                                                                self.SPS01[0,e[0]].UpdateStatus()
                                                                                self.SPS01[0,e[1]].UpdateStatus()
                                                                            if self.SPS01[0,e[0]].FlagIsDone or self.SPS01[0,e[1]].FlagIsDone:
                                                                                for s in range(len(e[0])):
                                                                                    if self.SPS01[0,e[s]].FlagIsDone == True:
                                                                                        self.SPS01[0,e[s]].displaymovementstop()
                                                                                        f=e 
                                                                                        f[s]=[] 
                                                                                        while self.SPS01[0,f[0]].FlagIsMoving:
                                                                                            self.SPS01[0,f[0]].UpdateStatus()
                                                                                        if self.SPS01[0,f[0]].FlagIsDone:
                                                                                            self.SPS01[0,f[0]].displaymovementstop()
                                                                                        break
                                                                break
                                                    break
                                        break
                            break
        elif len(args) == 11:
            i1=args[2]  
            i2=args[3] 
            i3=args[4] 
            i4=args[5] 
            i5=args[6] 
            i6=args[7] 
            i7=args[8] 
            i8=args[9] 
            i=[i1, i2, i3, i4, i5, i6, i7, i8]   # #i=args[2:len(args)-2]
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True and self.SPS01[0,i8].FlagIsMoving == True:
                while self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True and self.SPS01[0,i8].FlagIsMoving == True:
                    self.SPS01[0,i1].UpdateStatus() 
                    self.SPS01[0,i2].UpdateStatus() 
                    self.SPS01[0,i3].UpdateStatus() 
                    self.SPS01[0,i4].UpdateStatus() 
                    self.SPS01[0,i5].UpdateStatus() 
                    self.SPS01[0,i6].UpdateStatus() 
                    self.SPS01[0,i7].UpdateStatus() 
                    self.SPS01[0,i8].UpdateStatus()
                if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True or self.SPS01[0,i6].FlagIsDone == True or self.SPS01[0,i7].FlagIsDone == True or self.SPS01[0,i8].FlagIsDone == True:
                    for j in range(len(i[0])):
                        if self.SPS01[0,i(j)].FlagIsDone == True:
                            self.SPS01[0,i[j]].displaymovementstop()
                            a=i 
                            a[j]=[]  
                            while self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True and self.SPS01[0,a[4]].FlagIsMoving == True and self.SPS01[0,a[5]].FlagIsMoving == True and self.SPS01[0,a[6]].FlagIsMoving == True:
                                    self.SPS01[0,a[0]].UpdateStatus() 
                                    self.SPS01[0,a[1]].UpdateStatus() 
                                    self.SPS01[0,a[2]].UpdateStatus() 
                                    self.SPS01[0,a[3]].UpdateStatus() 
                                    self.SPS01[0,a[4]].UpdateStatus() 
                                    self.SPS01[0,a[5]].UpdateStatus() 
                                    self.SPS01[0,a[6]].UpdateStatus()
                            if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True or self.SPS01[0,a[4]].FlagIsDone == True or self.SPS01[0,a[5]].FlagIsDone == True or self.SPS01[0,a[6]].FlagIsDone == True:
                                for k in range(len(a[0])):
                                    if self.SPS01[0,a[k]].FlagIsDone == True:
                                        self.SPS01[0,a[k]].displaymovementstop()
                                        b=a 
                                        b[k]=[] 
                                        while self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True and self.SPS01[0,b[3]].FlagIsMoving == True and self.SPS01[0,b[4]].FlagIsMoving == True and self.SPS01[0,b[5]].FlagIsMoving == True:
                                            self.SPS01[0,b[0]].UpdateStatus() 
                                            self.SPS01[0,b[1]].UpdateStatus() 
                                            self.SPS01[0,b[2]].UpdateStatus() 
                                            self.SPS01[0,b[3]].UpdateStatus() 
                                            self.SPS01[0,b[4]].UpdateStatus() 
                                            self.SPS01[0,b[5]].UpdateStatus()
                                        if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True or self.SPS01[0,b[3]].FlagIsDone == True or self.SPS01[0,b[4]].FlagIsDone == True or self.SPS01[0,b[5]].FlagIsDone == True:
                                            for p in range(len(b[0])):
                                                if self.SPS01[0,b[p]].FlagIsDone == True:
                                                    self.SPS01[0,b[p]].displaymovementstop()
                                                    c=b 
                                                    c[p]=[] 
                                                    while self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving and self.SPS01[0,c[2]].FlagIsMoving and self.SPS01[0,c[3]].FlagIsMoving and self.SPS01[0,c[4]].FlagIsMoving:
                                                        self.SPS01[0,c[0]].UpdateStatus() 
                                                        self.SPS01[0,c[1]].UpdateStatus() 
                                                        self.SPS01[0,c[2]].UpdateStatus() 
                                                        self.SPS01[0,c[3]].UpdateStatus() 
                                                        self.SPS01[0,c[4]].UpdateStatus()
                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True or self.SPS01[0,c[2]].FlagIsDone == True or self.SPS01[0,c[3]].FlagIsDone == True or self.SPS01[0,c[4]].FlagIsDone == True:
                                                        for q in range(len(c[0])):
                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                d=c 
                                                                d[q]=[] 
                                                                while self.SPS01[0,d[0]].FlagIsMoving and self.SPS01[0,d[1]].FlagIsMoving and self.SPS01[0,d[2]].FlagIsMoving and self.SPS01[0,d[3]].FlagIsMoving:
                                                                    self.SPS01[0,d[0]].UpdateStatus() 
                                                                    self.SPS01[0,d[1]].UpdateStatus() 
                                                                    self.SPS01[0,d[2]].UpdateStatus() 
                                                                    self.SPS01[0,d[3]].UpdateStatus()
                                                                if self.SPS01[0,d[0]].FlagIsDone or self.SPS01[0,d[1]].FlagIsDone or self.SPS01[0,d[2]].FlagIsDone or self.SPS01[0,d[3]].FlagIsDone:
                                                                    for r in range(len(d[0])):
                                                                        if self.SPS01[0,d[r]].FlagIsDone == True:
                                                                            self.SPS01[0,d[r]].displaymovementstop()
                                                                            e=d 
                                                                            e[r]=[] 
                                                                            while self.SPS01[0,e[0]].FlagIsMoving and self.SPS01[0,e[1]].FlagIsMoving and self.SPS01[0,e[2]].FlagIsMoving:
                                                                                self.SPS01[0,e[0]].UpdateStatus() 
                                                                                self.SPS01[0,e[1]].UpdateStatus() 
                                                                                self.SPS01[0,e[2]].UpdateStatus()
                                                                            if self.SPS01[0,e[0]].FlagIsDone or self.SPS01[0,e[1]].FlagIsDone or self.SPS01[0,e[2]].FlagIsDone:
                                                                                for s in range(len(e[0])):
                                                                                    if self.SPS01[0,e[s]].FlagIsDone == True:
                                                                                        self.SPS01[0,e[s]].displaymovementstop()
                                                                                        f=e 
                                                                                        f[s]=[] 
                                                                                        while self.SPS01[0,f[0]].FlagIsMoving and self.SPS01[0,f[1]].FlagIsMoving:
                                                                                            self.SPS01[0,f[0]].UpdateStatus() 
                                                                                            self.SPS01[0,f[1]].UpdateStatus()
                                                                                        if self.SPS01[0,f[0]].FlagIsDone or self.SPS01[0,f[1]].FlagIsDone:
                                                                                            for t in range(len(f[0])):
                                                                                                if self.SPS01[0,f[t]].FlagIsDone:
                                                                                                    self.SPS01[0,f[t]].displaymovementstop()
                                                                                                    g=f 
                                                                                                    g[t]=[] 
                                                                                                    while self.SPS01[0,g[0]].FlagIsMoving:
                                                                                                        self.SPS01[0,g[0]].UpdateStatus()
                                                                                                    if self.SPS01[0,g[0]].FlagIsDone:
                                                                                                        self.SPS01[0,g[0]].displaymovementstop()
                                                                                                    break
                                                                                        break
                                                                            break
                                                                break
                                                    break
                                        break
                            break


    ## Listener Function : Display the first device to be done and Stop (called in MulMove2)
    def CheckFirstDoneStop(self,*args):
        if len(args) == 4: ## only one syringe in motion (=numb input + self + 2more input (source and event))   
            i1=args[2] ##argsg doesnt include the self, so its size is len(args)-1. The index is the last.
            if self.SPS01[0,i1].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours                   
                for i in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break
                    elif self.SPS01[0,i1].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                    if self.SPS01[0,i1].FlagIsDone == True:
                        self.SPS01[0,i1].displaymovementstop()
                        break
                    time.sleep(scan_rate)
        elif len(args) == 5: ## 2 syringes
                i1=args[2] 
                i2=args[3]
                i=[i1, i2] 
                if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True:
                    scan_rate=0.1 ##the scan rate of the counter
                    target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours        
                    for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                        if self.Stop == True:
                            self.StopBoard()
                            break ## counter 1
                        elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True:
                            self.SPS01[0,i1].UpdateStatus()
                            self.SPS01[0,i2].UpdateStatus()
                        if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True:
                            for j in range(len(i[0])): ##search for first device to be done
                                if self.SPS01[0,i[j]].FlagIsDone == True:
                                    self.SPS01[0,i[j]].displaymovementstop()
                                    a=i
                                    a[j]=[]
                                    for count2 in range(target):
                                        if self.Stop == True:
                                            self.StopBoard()
                                            break ##counter 2
                                        elif self.SPS01[0,a[0]].FlagIsMoving == True:
                                            self.SPS01[0,a[0]].UpdateStatus()
                                        if self.SPS01[0,a[0]].FlagIsDone == True:
                                            self.SPS01[0,a[0]].displaymovementstop()
                                            break ##counter 2
                                        time.sleep(scan_rate)
                                    break ## j search of first device to be done 
                            break ## counter 1
                        time.sleep(scan_rate)
        elif len(args) == 6: ## 3 syringes
            i1=args[2] 
            i2=args[3]
            i3=args[4]
            i=[i1, i2, i3] 
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours
                for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break ## counter 1
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i2].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                    if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True:
                        for j in range(len(i[0])):
                            if self.SPS01[0,i(j)].FlagIsDone == True:
                                self.SPS01[0,i(j)].displaymovementstop()
                                a=i
                                a[j]=[] ## a=[i2 i3] for j=1, a=[i1 i3] for j=2, a=[i1 i2] for j=3
                                for count2 in range(target):
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break ## counter 2
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True:
                                        self.SPS01[0,a[0]].UpdateStatus()
                                        self.SPS01[0,a[1]].UpdateStatus()
                                    if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,a[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                for count3 in range(target):
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break ##counter 3
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True:
                                                        self.SPS01[0,b[0]].UpdateStatus()
                                                    if self.SPS01[0,b[0]].FlagIsDone == True:
                                                        self.SPS01[0,b[0]].displaymovementstop()
                                                        break ##counter 3
                                                    time.sleep(scan_rate)
                                                break ## k search of first device to be done 
                                        break ## counter 2
                                    time.sleep(scan_rate)
                                break ## j search of first device to be done 
                        break ## counter 1
                    time.sleep(scan_rate)
            
            
        elif len(args) == 7: ## 4 syringes
            i1=args[2] 
            i2=args[3]
            i3=args[4]
            i4=args[5]
            i=[i1, i2, i3, i4] 
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours                   
                for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break ## counter 1
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i2].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                        self.SPS01[0,i4].UpdateStatus() 
                    if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True:
                        for j in range(len(i[0])):
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPS01[0,i[j]].displaymovementstop()
                                a=i
                                a[j]=[] 
                                scan_rate=0.1 ##the scan rate of the counter
                                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours          
                                for count2 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break ## counter 2
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True:
                                        self.SPS01[0,a[0]].UpdateStatus()
                                        self.SPS01[0,a[1]].UpdateStatus()
                                        self.SPS01[0,a[2]].UpdateStatus()    
                                    if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,a[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                scan_rate=0.1 ##the scan rate of the counter
                                                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours 
                                                for count3 in range(target):
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break ## counter 3
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True:
                                                        self.SPS01[0,b[0]].UpdateStatus()
                                                        self.SPS01[0,b[1]].UpdateStatus()
                                                    if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True:
                                                        for p in range(len(b[0])):
                                                            if self.SPS01[0,b[p]].FlagIsDone == True:
                                                                self.SPS01[0,b[p]].displaymovementstop()
                                                                c=b
                                                                c[p]=[]
                                                                for count4 in range(target):
                                                                    if self.Stop == True:
                                                                        self.StopBoard()
                                                                        break ## counter 4
                                                                    elif self.SPS01[0,c[0]].FlagIsMoving == True:
                                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                                    if self.SPS01[0,c[0]].FlagIsDone == True:
                                                                        self.SPS01[0,c[0]].displaymovementstop()
                                                                        break ## counter 4
                                                                    time.sleep(scan_rate)
                                                                break ## p search of first device to be done
                                                        break ##counter 3
                                                    time.sleep(scan_rate)
                                                break ## k search of first device to be done
                                        break ##counter 2
                                    time.sleep(scan_rate)
                                break ## j search of first device to be done
                        break ## counter 1
                    time.sleep(scan_rate)
                                                    
        elif len(args) == 8: ## 5 syringes
            i1=args[2] 
            i2=args[3]
            i3=args[4]
            i4=args[5]
            i5=args[6]
            i=[i1, i2, i3, i4, i5] 
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours                   
                for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break ## counter 1
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i2].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                        self.SPS01[0,i4].UpdateStatus()
                        self.SPS01[0,i5].UpdateStatus()                            
                    if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True:
                        for j in range(len(i[0])):
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPS01[0,i[j]].displaymovementstop()
                                a=i
                                a[j]=[] 
                                for count2 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break ## counter 2
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True:
                                        self.SPS01[0,a(0)].UpdateStatus()
                                        self.SPS01[0,a(1)].UpdateStatus()
                                        self.SPS01[0,a(2)].UpdateStatus()
                                        self.SPS01[0,a(3)].UpdateStatus()                                            
                                    if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,a[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                for count3 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break ## counter 3
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True:
                                                        self.SPS01[0,b[0]].UpdateStatus()
                                                        self.SPS01[0,b[1]].UpdateStatus()
                                                        self.SPS01[0,b[2]].UpdateStatus()                                                            
                                                    if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[1,b[2]].FlagIsDone == True:
                                                        for p in range(len(b[0])):
                                                            if self.SPS01[0,b[p]].FlagIsDone == True:
                                                                self.SPS01[0,b[p]].displaymovementstop()
                                                                c=b
                                                                c[p]=[]
                                                                for count4 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                    if self.Stop == True:
                                                                        self.StopBoard()
                                                                        break ## counter 4
                                                                    elif self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving:
                                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                                        self.SPS01[0,c[1]].UpdateStatus()                                                                            
                                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True:
                                                                        for q in range(len(c[0])):
                                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                                d=c
                                                                                d[q]=[]
                                                                                for count5 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                    if self.Stop == True:
                                                                                        self.StopBoard()
                                                                                        break ## counter 5
                                                                                    elif self.SPS01[0,d[0]].FlagIsMoving:
                                                                                        self.SPS01[0,d[0]].UpdateStatus()                                                                                            
                                                                                    if self.SPS01[0,d[0]].FlagIsDone:
                                                                                        self.SPS01[0,d[0]].displaymovementstop()
                                                                                        break ##counter 5
                                                                                    time.sleep(scan_rate)
                                                                                break ## q search of first device to be done
                                                                        break ## counter 4
                                                                    time.sleep(scan_rate)
                                                                break ## p search of first device to be done
                                                        break ## counter 3
                                                    time.sleep(scan_rate)
                                                break ## k search of first device to be done
                                        break ## counter 2
                                    time.sleep(scan_rate)
                                break ## j search of first device to be done
                        break ## counter 1
                    time.sleep(scan_rate)
                                                                
        elif len(args) == 9: ## 6 syringes
            i1=args[2] 
            i2=args[3]
            i3=args[4]
            i4=args[5]
            i5=args[6]
            i6=args[7]
            i=[i1, i2, i3, i4, i5, i6] 
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours                   
                for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break ## counter 1
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i2].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                        self.SPS01[0,i4].UpdateStatus()
                        self.SPS01[0,i5].UpdateStatus()
                        self.SPS01[0,i6].UpdateStatus()                            
                    if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True or self.SPS01[0,i6].FlagIsDone == True:
                        for j in range(len(i[0])):
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPS01[0,i[j]].displaymovementstop()
                                a=i
                                a[j]=[] 
                                for count2 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break ## counter 2
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True and self.SPS01[0,a[4]].FlagIsMoving == True:
                                        self.SPS01[0,a[0]].UpdateStatus()
                                        self.SPS01[0,a[1]].UpdateStatus()
                                        self.SPS01[0,a[2]].UpdateStatus()
                                        self.SPS01[0,a[3]].UpdateStatus()
                                        self.SPS01[0,a[4]].UpdateStatus()                                            
                                    if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True or self.SPS01[0,a[4]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,a[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                for count3 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break ## counter 3
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True and self.SPS01[0,b[3]].FlagIsMoving == True:
                                                        self.SPS01[0,b[0]].UpdateStatus()
                                                        self.SPS01[0,b[1]].UpdateStatus()
                                                        self.SPS01[0,b[2]].UpdateStatus()
                                                        self.SPS01[0,b[3]].UpdateStatus()                                                            
                                                    if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True or self.SPS01[0,b[3]].FlagIsDone == True:
                                                        for p in range(len(b[0])):
                                                            if self.SPS01[0,b[p]].FlagIsDone == True:
                                                                self.SPS01[0,b[p]].displaymovementstop()
                                                                c=b
                                                                c[p]=[]
                                                                for count4 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                    if self.Stop == True:
                                                                        self.StopBoard()
                                                                        break ## counter 4
                                                                    elif self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving and self.SPS01[0,c[2]].FlagIsMoving:
                                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                                        self.SPS01[0,c[1]].UpdateStatus()
                                                                        self.SPS01[0,c[2]].UpdateStatus()                                                                            
                                                                    if self.SPS01[0,c(1)].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True or self.SPS01[0,c[2]].FlagIsDone == True:
                                                                        for q in range(len(c[0])):
                                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                                self.SPS01[1,c(q)].displaymovementstop()
                                                                                d=c
                                                                                d[q]=[]
                                                                                for count5 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                    if self.Stop == True:
                                                                                        self.StopBoard()
                                                                                        break ## counter 5
                                                                                    elif self.SPS01[0,d[0]].FlagIsMoving and self.SPS01[0,d[1]].FlagIsMoving:
                                                                                        self.SPS01[0,d[0]].UpdateStatus()
                                                                                        self.SPS01[0,d[1]].UpdateStatus()                                                                                            
                                                                                    if self.SPS01[0,d[0]].FlagIsDone or self.SPS01[0,d[1]].FlagIsDone:
                                                                                        for r in range(len(d[0])):
                                                                                            if self.SPS01[0,d[r]].FlagIsDone == True:
                                                                                                self.SPS01[0,d[r]].displaymovementstop()
                                                                                                e=d
                                                                                                e[r]=[]
                                                                                                for count6 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                                    if self.Stop == True:
                                                                                                        self.StopBoard()
                                                                                                        break ## counter 6
                                                                                                    elif self.SPS01[0,e[0]].FlagIsMoving:
                                                                                                        self.SPS01[0,e[0]].UpdateStatus()                                                                                                            
                                                                                                    if self.SPS01[0,e[0]].FlagIsDone:
                                                                                                        self.SPS01[0,e[0]].displaymovementstop()
                                                                                                        break ## counter 6
                                                                                                    time.sleep(scan_rate)
                                                                                                break ## r search of first device to be done
                                                                                        break ## counter 5
                                                                                    time.sleep(scan_rate)
                                                                                break ## q search of first device to be done
                                                                        break ##counter 4
                                                                    time.sleep(scan_rate)
                                                                break ## p search of first device to be done
                                                        break ## Counter 3
                                                    time.sleep(scan_rate)
                                                break ## k search of first device to be done
                                        break ## counter 2
                                    time.sleep(scan_rate)
                                break ## j search of first device to be done
                        break ## counter 1
                    time.sleep(scan_rate)
                                                        
        elif len(args) == 10: ##7 syringes
            i1=args[2] 
            i2=args[3]
            i3=args[4]
            i4=args[5]
            i5=args[6]
            i6=args[7]
            i7=args[8]
            i=[i1, i2, i3, i4, i5, i6, i7] 
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours                   
                for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break ## counter 1
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i2].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                        self.SPS01[0,i4].UpdateStatus()
                        self.SPS01[0,i5].UpdateStatus()
                        self.SPS01[0,i6].UpdateStatus()
                        self.SPS01[0,i7].UpdateStatus()
                    if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True or self.SPS01[0,i6].FlagIsDone == True or self.SPS01[0,i7].FlagIsDone == True:
                        for j in range(len(i[0])):
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPS01[0,i[j]].displaymovementstop()
                                a=i
                                a[j]=[] 
                                for count2 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break ## counter 2
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True and self.SPS01[0,a[4]].FlagIsMoving == True and self.SPS01[0,a[5]].FlagIsMoving == True:
                                        self.SPS01[0,a[0]].UpdateStatus()
                                        self.SPS01[0,a[1]].UpdateStatus()
                                        self.SPS01[0,a[2]].UpdateStatus()
                                        self.SPS01[0,a[3]].UpdateStatus()
                                        self.SPS01[0,a[4]].UpdateStatus()
                                        self.SPS01[0,a[5]].UpdateStatus()
                                    if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True or self.SPS01[0,a[4]].FlagIsDone == True or self.SPS01[0,a[5]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,a[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                for count3 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break ## counter 3
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True and self.SPS01[0,b[3]].FlagIsMoving == True and self.SPS01[0,b[4]].FlagIsMoving == True:
                                                        self.SPS01[0,b[0]].UpdateStatus()
                                                        self.SPS01[0,b[1]].UpdateStatus()
                                                        self.SPS01[0,b[2]].UpdateStatus()
                                                        self.SPS01[0,b[3]].UpdateStatus()
                                                        self.SPS01[0,b[4]].UpdateStatus()
                                                    if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True or self.SPS01[0,b[3]].FlagIsDone == True or self.SPS01[0,b[4]].FlagIsDone == True:
                                                        for p in range(len(b[0])):
                                                            if self.SPS01[0,b[p]].FlagIsDone == True:
                                                                self.SPS01[0,b[p]].displaymovementstop()
                                                                c=b
                                                                c[p]=[]
                                                                for count4 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                    if self.Stop == True:
                                                                        self.StopBoard()
                                                                        break ## counter 4
                                                                    elif self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving and self.SPS01[0,c[2]].FlagIsMoving and self.SPS01[0,c[3]].FlagIsMoving:
                                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                                        self.SPS01[0,c[1]].UpdateStatus()
                                                                        self.SPS01[0,c[2]].UpdateStatus()
                                                                        self.SPS01[0,c[3]].UpdateStatus()
                                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True or self.SPS01[0,c[2]].FlagIsDone == True or self.SPS01[0,c[3]].FlagIsDone == True:
                                                                        for q in range(len(c[0])):
                                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                                d=c
                                                                                d[q]=[]
                                                                                for count5 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                    if self.Stop == True:
                                                                                        self.StopBoard()
                                                                                        break ## counter 5
                                                                                    elif self.SPS01[0,d[0]].FlagIsMoving and self.SPS01[0,d[1]].FlagIsMoving and self.SPS01[0,d[2]].FlagIsMoving:
                                                                                        self.SPS01[0,d[0]].UpdateStatus()
                                                                                        self.SPS01[0,d[1]].UpdateStatus()
                                                                                        self.SPS01[0,d[2]].UpdateStatus()
                                                                                    if self.SPS01[0,d[0]].FlagIsDone or self.SPS01[0,d[1]].FlagIsDone or self.SPS01[0,d[2]].FlagIsDone:
                                                                                        for r in range(len(d[0])):
                                                                                            if self.SPS01[0,d[r]].FlagIsDone == True:
                                                                                                self.SPS01[0,d[r]].displaymovementstop()
                                                                                                e=d
                                                                                                e[r]=[]
                                                                                                for count6 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                                    if self.Stop == True:
                                                                                                        self.StopBoard()
                                                                                                        break ## counter 6
                                                                                                    elif self.SPS01[0,e[0]].FlagIsMoving and self.SPS01[0,e[1]].FlagIsMoving:
                                                                                                        self.SPS01[0,e[0]].UpdateStatus()
                                                                                                        self.SPS01[0,e[1]].UpdateStatus()
                                                                                                    if self.SPS01[0,e[0]].FlagIsDone or self.SPS01[0,e[1]].FlagIsDone:
                                                                                                        for s in range(len(e[0])):
                                                                                                            if self.SPS01[0,e[s]].FlagIsDone == True:
                                                                                                                self.SPS01[0,e[s]].displaymovementstop()
                                                                                                                f=e
                                                                                                                f[s]=[]
                                                                                                                for count7 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                                                    if self.Stop == True:
                                                                                                                        self.StopBoard()
                                                                                                                        break ## counter 7
                                                                                                                    elif self.SPS01[0,f[0]].FlagIsMoving:
                                                                                                                        self.SPS01[0,f[0]].UpdateStatus()
                                                                                                                    if self.SPS01[0,f[0]].FlagIsDone:
                                                                                                                        self.SPS01[0,f[0]].displaymovementstop()
                                                                                                                        break ## counter 7
                                                                                                                    time.sleep(scan_rate)
                                                                                                                break ## s search of first device to be done
                                                                                                        break ## counter 6
                                                                                                    time.sleep(scan_rate)
                                                                                                break ## r search of first device to be done
                                                                                        break ## counter 5
                                                                                    time.sleep(scan_rate)
                                                                                break ## q search of first device to be done
                                                                        break ## counter 4
                                                                    time.sleep(scan_rate)
                                                                break ## p search of first device to be done
                                                        break ## counter 3
                                                    time.sleep(scan_rate)
                                                break ## k search of first device to be done
                                        break ## counter 2
                                    time.sleep(scan_rate)
                                break ## j search of first device to be done
                        break ## counter 1
                    time.sleep(scan_rate)
                        
        elif len(args) == 11: ##8 syringes (impossible - max is 7)
            i1=args[2] 
            i2=args[3]
            i3=args[4]
            i4=args[5]
            i5=args[6]
            i6=args[7]
            i7=args[8]
            i8=args[9]
            i=[i1, i2, i3, i4, i5, i6, i7, i8] ##i=args[3:len(args)-1]
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True and self.SPS01[0,i8].FlagIsMoving == True:
                scan_rate=0.1 ##the scan rate of the counter
                target=(48)*60*60#scan_rate ##this is the final time of the counter. It is equal to max 48 hours                   
                for count1 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break ## counter 1
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True and self.SPS01[0,i4].FlagIsMoving == True and self.SPS01[0,i5].FlagIsMoving == True and self.SPS01[0,i6].FlagIsMoving == True and self.SPS01[0,i7].FlagIsMoving == True and self.SPS01[0,i8].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i2].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                        self.SPS01[0,i4].UpdateStatus()
                        self.SPS01[0,i5].UpdateStatus()
                        self.SPS01[0,i6].UpdateStatus()
                        self.SPS01[0,i7].UpdateStatus()
                        self.SPS01[0,i8].UpdateStatus()
                    if self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True or self.SPS01[0,i4].FlagIsDone == True or self.SPS01[0,i5].FlagIsDone == True or self.SPS01[0,i6].FlagIsDone == True or self.SPS01[0,i7].FlagIsDone == True or self.SPS01[0,i8].FlagIsDone == True:
                        for j in range(len(i[0])):
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPS01[0,i[j]].displaymovementstop()
                                a=i
                                a[j]=[] 
                                for count2 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break ## counter 2
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True and self.SPS01[0,a[2]].FlagIsMoving == True and self.SPS01[0,a[3]].FlagIsMoving == True and self.SPS01[0,a[4]].FlagIsMoving == True and self.SPS01[0,a[5]].FlagIsMoving == True and self.SPS01[0,a[6]].FlagIsMoving == True:
                                        self.SPS01[0,a[0]].UpdateStatus()
                                        self.SPS01[0,a[1]].UpdateStatus()
                                        self.SPS01[0,a[2]].UpdateStatus()
                                        self.SPS01[0,a[3]].UpdateStatus()
                                        self.SPS01[0,a[4]].UpdateStatus()
                                        self.SPS01[0,a[5]].UpdateStatus()
                                        self.SPS01[0,a[6]].UpdateStatus()
                                    if self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True or self.SPS01[0,a[2]].FlagIsDone == True or self.SPS01[0,a[3]].FlagIsDone == True or self.SPS01[0,a[4]].FlagIsDone == True or self.SPS01[0,a[5]].FlagIsDone == True or self.SPS01[0,a[6]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                for count3 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break ## counter 3
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True and self.SPS01[0,b[1]].FlagIsMoving == True and self.SPS01[0,b[2]].FlagIsMoving == True and self.SPS01[0,b[3]].FlagIsMoving == True and self.SPS01[0,b[4]].FlagIsMoving == True and self.SPS01[0,b[5]].FlagIsMoving == True:
                                                        self.SPS01[0,b[0]].UpdateStatus()
                                                        self.SPS01[0,b[1]].UpdateStatus()
                                                        self.SPS01[0,b[2]].UpdateStatus()
                                                        self.SPS01[0,b[3]].UpdateStatus()
                                                        self.SPS01[0,b[4]].UpdateStatus()
                                                        self.SPS01[0,b[5]].UpdateStatus()
                                                    if self.SPS01[0,b[0]].FlagIsDone == True or self.SPS01[0,b[1]].FlagIsDone == True or self.SPS01[0,b[2]].FlagIsDone == True or self.SPS01[0,b[3]].FlagIsDone == True or self.SPS01[0,b[4]].FlagIsDone == True or self.SPS01[0,b[5]].FlagIsDone == True:
                                                        for p in range(len(b[0])):
                                                            if self.SPS01[0,b[p]].FlagIsDone == True:
                                                                self.SPS01[0,b[p]].displaymovementstop()
                                                                c=b
                                                                c[p]=[]
                                                                for count4 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                    if self.Stop == True:
                                                                        self.StopBoard()
                                                                        break ## counter 4
                                                                    elif self.SPS01[0,c[0]].FlagIsMoving == True and self.SPS01[0,c[1]].FlagIsMoving and self.SPS01[0,c[2]].FlagIsMoving and self.SPS01[0,c[3]].FlagIsMoving and self.SPS01[0,c[4]].FlagIsMoving:
                                                                        self.SPS01[0,c[0]].UpdateStatus()
                                                                        self.SPS01[0,c[1]].UpdateStatus()
                                                                        self.SPS01[0,c[2]].UpdateStatus()
                                                                        self.SPS01[0,c[3]].UpdateStatus()
                                                                        self.SPS01[0,c[4]].UpdateStatus()                                                                           
                                                                    if self.SPS01[0,c[0]].FlagIsDone == True or self.SPS01[0,c[1]].FlagIsDone == True or self.SPS01[0,c[2]].FlagIsDone == True or self.SPS01[0,c[3]].FlagIsDone == True or self.SPS01[0,c[4]].FlagIsDone == True:
                                                                        for q in range(len(c[0])):
                                                                            if self.SPS01[0,c[q]].FlagIsDone == True:
                                                                                self.SPS01[0,c[q]].displaymovementstop()
                                                                                d=c
                                                                                d[q]=[]
                                                                                for count5 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                    if self.Stop == True:
                                                                                        self.StopBoard()
                                                                                        break ## counter 5
                                                                                    elif self.SPS01[0,d[0]].FlagIsMoving and self.SPS01[0,d[1]].FlagIsMoving and self.SPS01[0,d[2]].FlagIsMoving and self.SPS01[0,d[3]].FlagIsMoving:
                                                                                        self.SPS01[0,d[0]].UpdateStatus()
                                                                                        self.SPS01[0,d[1]].UpdateStatus()
                                                                                        self.SPS01[0,d[2]].UpdateStatus()
                                                                                        self.SPS01[0,d[3]].UpdateStatus()
                                                                                    if self.SPS01[0,d[0]].FlagIsDone or self.SPS01[0,d[1]].FlagIsDone or self.SPS01[0,d[2]].FlagIsDone or self.SPS01[0,d[3]].FlagIsDone:
                                                                                        for r in range(len(d[0])):
                                                                                            if self.SPS01[0,d[r]].FlagIsDone == True:
                                                                                                self.SPS01[0,d[r]].displaymovementstop()
                                                                                                e=d
                                                                                                e[r]=[]
                                                                                                for count6 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                                    if self.Stop == True:
                                                                                                        self.StopBoard()
                                                                                                        break ## counter 6
                                                                                                    elif self.SPS01[0,e[0]].FlagIsMoving and self.SPS01[0,e[1]].FlagIsMoving and self.SPS01[0,e[2]].FlagIsMoving:
                                                                                                        self.SPS01[0,e[0]].UpdateStatus()
                                                                                                        self.SPS01[0,e[1]].UpdateStatus()
                                                                                                        self.SPS01[0,e[2]].UpdateStatus()
                                                                                                    if self.SPS01[0,e[0]].FlagIsDone or self.SPS01[0,e[1]].FlagIsDone or self.SPS01[0,e[2]].FlagIsDone:
                                                                                                        for s in range(len(e[0])):
                                                                                                            if self.SPS01[0,e[s]].FlagIsDone == True:
                                                                                                                self.SPS01[0,e[s]].displaymovementstop()
                                                                                                                f=e
                                                                                                                f[s]=[]
                                                                                                                for count7 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                                                    if self.Stop == True:
                                                                                                                        self.StopBoard()
                                                                                                                        break ## counter 7
                                                                                                                    elif self.SPS01[0,f[0]].FlagIsMoving and self.SPS01[0,f[1]].FlagIsMoving:
                                                                                                                        self.SPS01[0,f[0]].UpdateStatus()
                                                                                                                        self.SPS01[0,f[1]].UpdateStatus()
                                                                                                                    if self.SPS01[0,f[0]].FlagIsDone or self.SPS01[0,f[1]].FlagIsDone:
                                                                                                                        for t in range(len(f[0])):
                                                                                                                            if self.SPS01[0,f[t]].FlagIsDone:
                                                                                                                                self.SPS01[0,f[t]].displaymovementstop()
                                                                                                                                g=f
                                                                                                                                g[t]=[]
                                                                                                                                for count8 in range(target): ##this is a counter clock to check if the stop_status variable has changed
                                                                                                                                    if self.Stop == True:
                                                                                                                                        self.StopBoard()
                                                                                                                                        break ## counter 8
                                                                                                                                    elif self.SPS01[0,g(0)].FlagIsMoving:
                                                                                                                                        self.SPS01[0,g[0]].UpdateStatus()
                                                                                                                                    if self.SPS01[0,g[0]].FlagIsDone:
                                                                                                                                        self.SPS01[0,g[0]].displaymovementstop()
                                                                                                                                        break ## counter 8
                                                                                                                                    time.sleep(scan_rate)
                                                                                                                                break ## t search of first device to be done
                                                                                                                        break ##counter 7
                                                                                                                    time.sleep(scan_rate)
                                                                                                                break ## s search of first device to be done
                                                                                                        break ## counter 6
                                                                                                    time.sleep(scan_rate)
                                                                                                break ## r search of first device to be done
                                                                                        break ## counter 5
                                                                                    time.sleep(scan_rate)
                                                                                break ## q search of first device to be done
                                                                        break ## counter 4
                                                                    time.sleep(scan_rate)
                                                                break ## p search of first device to be done
                                                        break ##counter 3
                                                    time.sleep(scan_rate)
                                                break ## k search of first device to be done
                                        break ## counter 2
                                    time.sleep(scan_rate)
                                break ## j search of first device to be done
                        break ##counter 1
                    time.sleep(scan_rate)
    ## TODO ##

    ##  Set Valves
    def SetValves(self,d1,v11,v12,v13,v14,d2,v21,v22,v23,v24):
        pass
    ## TODO ##

    ## Check First Done Stop M
    def CheckFirstDoneStopM(self,args):
        pass
    ## TODO ##

    ## Pause : same as stop but with different comment
    def PauseBoard (self):
        pass
    ## TODO ##

    ## Listener Function : Display the first device to be done and Stop and Pause (called in MulMove3)
    def CheckFirstDoneStopPause(self,args):
      if len(args) == 6: #only one syringe in motion (=numb input + self + 2more input (source and event))   
            i1=args[2] #vararging doesn't include the self, so its size is nargin-1. The index is the last.
            d1=args[3]
            v1=args[4]
            if self.SPS01[0,i1].FlagIsMoving == True:  
                scan_rate=0.1; #the scan rate of the counter
                target=(48)*60*60#scan_rate; #this is the final time of the counter. It is equal to max 48 hours                   
                for count1 in range(target): #this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        com=self.StopBoard()
                        break #counter1
                    elif self.Pause == True:
                        self.PauseBoard()
                        for count_pause1 in range(target):
                            if self.Stop == True:                                                              
                                break #count_pause1
                            elif self.Resume == True:
                                self.ClockResume = clock
                                comment=[num2str(self.ClockResume(4)) , ':' , num2str(self.ClockResume(5)) ,':' ,num2str(self.ClockResume(6)), ' Interface resumed by the user.'] 
                                diary on
                                disp(comment)
                                diary off 
                                self.SPS01[0,i1].UpdateStatus()
                                self.MulMove3[d1,v1]                                 
                                self.flag_break_countpause = 1
                                break #count_pause1
                            time.sleep(scan_rate)
                    elif self.SPS01{0,i1}.FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                    if self.flag_break_countpause == 1:
                        break #counter1
                    elif self.SPS01[0,i1].FlagIsDone == True: 
                        self.SPS01[0,i1].displaymovementstop()
                        break #counter1
                    time.sleep(scan_rate)
        elif nargin == 9: # 2 syringes
            i1=args[2] 
            d1=args[3]
            v1=args[4]
            i2=args[5]
            d2=args[6]
            v2=args[7]
            i=[i1 i2]
            d=[d1 d2]
            v=[v1 v2]
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True: 
                scan_rate=0.1 #the scan rate of the counter
                target=(48)*60*60 #scan_rate; ##this is the final time of the counter. It is equal to max 48 hours        
                for count1 in range (target) #this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break # counter 1
                    elif self.Pause == True:
                        self.PauseBoard()
                        for count_pause1 in range (target):
                            if self.Stop == True:
                                break #count_pause1
                            elif self.Resume == True:
                                self.ClockResume = clock
                                comment=[num2str(self.ClockResume(4)) , ':' , num2str(self.ClockResume(5)) ,':' ,num2str(self.ClockResume(6)), ' Interface resumed by the user.'] 
                                diary on
                                disp(comment)
                                diary off  
                                self.SPS01[0,i1].UpdateStatus() #############################
                                self.SPSO1[0,i2].UpdateStatus() #############################
                                self.MulMove3[d1,v1,d2,v2]                                 
                                self.flag_break_countpause = 1
                                break #count_pause1
                            time.sleep(scan_rate)
                    elif self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True:
                        self.SPSO1[0,i1].UpdateStatus()
                        self.SPSO1[0,i2].UpdateStatus()
                    if self.flag_break_countpause == 1:
                        break #counter1                        
                    elif self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True:
                        for j in range(len(i[0])): #search for first device to be done
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPSO1[0,i[j]].displaymovementstop()
                                a=i
                                a(j)=[]
                                ad=d
                                ad(j)=[]
                                av=v
                                av(j)=[]
                                for count2 in range (target):
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break #counter 2
                                    elif self.Pause == True:
                                        self.PauseBoard()
                                        for count_pause1 in range (target):
                                            if self.Stop == True:
                                                break #count_pause1
                                            elif self.Resume == True:
                                                self.ClockResume = clock
                                                comment=[num2str(self.ClockResume(4)) , ':' , num2str(self.ClockResume(5)) ,':' ,num2str(self.ClockResume(6)), ' Interface resumed by the user.']
                                                diary on
                                                disp(comment)
                                                diary off  
                                                self.SPSO1[0,a(0)].UpdateStatus() #############################
                                                self.MulMove3[ad[0],av[0]];                                    
                                                self.flag_break_countpause = 1
                                                break #count_pause1
                                            time.sleep(scan_rate)
                                    elif self.SPS01[0,a(0)].FlagIsMoving == True:
                                        self.SPSO1[0,a(0)].UpdateStatus()
                                    if self.flag_break_countpause == 1:
                                        break #counter1  
                                    elif self.SPS01[0,a(0)].FlagIsDone == True:
                                        self.SPSO1[0,a(0)].displaymovementstop()
                                        break ##counter 2                                          
                                    time.sleep(scan_rate)                                          
                                break # j search of first device to be done                                                                        
                        break # counter 1
                    time.sleep(scan_rate)            
                
        elif nargin == 12: # 3 syringes
            i1=args[2] 
            d1=args[3]
            v1=args[4]
            i2=args[5]
            d2=args[6]
            v2=args[7]
            i3=args[8]
            d3=args[9]
            v3=args[10]
            i=[i1 i2 i3]
            d=[d1 d2 d3]
            v=[v1 v2 v3]
            if self.SPS01[0,i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True: 
                scan_rate=0.1; #the scan rate of the counter
                target=(48)*60*60 #scan_rate; ##this is the final time of the counter. It is equal to max 48 hours
                for count1 in range(target) #this is a counter clock to check if the stop_status variable has changed
                    if self.Stop == True:
                        self.StopBoard()
                        break # counter 1                            
                     elif self.Pause == True:
                        self.PauseBoard()
                        for count_pause1 in range(target):
                            if self.Stop == True:
                                break #count_pause1
                            elif self.Resume == True:
                                self.ClockResume = clock
                                comment=[num2str(self.ClockResume(4)) , ':' , num2str(self.ClockResume(5)) ,':' ,num2str(self.ClockResume(6)), ' Interface resumed by the user.'] 
                                diary on
                                disp(comment)
                                diary off  
                                self.SPSO1[0,i1].UpdateStatus() #############################
                                self.SPSO1[0,i2].UpdateStatus() #############################
                                self.SPS01[0,i3].UpdateStatus() #############################
                                self.MulMove3[d1,v1,d2,v2,d3,v3]                                    
                                self.flag_break_countpause = 1
                                break #count_pause1
                            time.sleep(scan_rate)
                    elif self.SPS01[0],i1].FlagIsMoving == True and self.SPS01[0,i2].FlagIsMoving == True and self.SPS01[0,i3].FlagIsMoving == True:
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i1].UpdateStatus()
                        self.SPS01[0,i3].UpdateStatus()
                    if self.flag_break_countpause == 1:
                        break #counter1  
                    elif self.SPS01[0,i1].FlagIsDone == True or self.SPS01[0,i2].FlagIsDone == True or self.SPS01[0,i3].FlagIsDone == True:
                        for j=1 in range(len(i[0])):
                            if self.SPS01[0,i[j]].FlagIsDone == True:
                                self.SPS01[0,i[j]].displaymovementstop()
                                a=i
                                a[j]=[]; # a=[i2 i3] for j=1, a=[i1 i3] for j=2, a=[i1 i2] for j=3
                                ad=d
                                ad[j]=[]
                                av=v
                                av[j]=[]
                                for count2 in range (target):
                                    if self.Stop == True:
                                        self.StopBoard()
                                        break # counter 2                                            
                                     elif self.Pause == True:
                                        self.PauseBoard()
                                        for count_pause1 in range (target):
                                            if self.Stop == True:
                                                break #count_pause1
                                            elif self.Resume == True:
                                                self.ClockResume = clock
                                                comment=[num2str(self.ClockResume(4)) , ':' , num2str(self.ClockResume(5)) ,':' ,num2str(self.ClockResume(6)), ' Interface resumed by the user.'] 
                                                diary on
                                                disp(comment)
                                                diary off  
                                                self.SPS01[0,a[0]].UpdateStatus() #############################
                                                self.SPS01[0,a[1]].UpdateStatus() #############################
                                                self.MulMove3[ad[1],av[1],ad[2],av[2]]                                 
                                                self.flag_break_countpause = 1
                                                break #count_pause1
                                            time.sleep(scan_rate)                                             
                                    elif self.SPS01[0,a[0]].FlagIsMoving == True and self.SPS01[0,a[1]].FlagIsMoving == True:
                                        self.SPSO1[0,a[0]].UpdateStatus()
                                        self.SPSO1[1,a[1]].UpdateStatus()
                                    if self.flag_break_countpause == 1:
                                        break #counter1  
                                    elif self.SPS01[0,a[0]].FlagIsDone == True or self.SPS01[0,a[1]].FlagIsDone == True:
                                        for k in range(len(a[0])):
                                            if self.SPS01[0,a[k]].FlagIsDone == True:
                                                self.SPS01[0,a[k]].displaymovementstop()
                                                b=a
                                                b[k]=[]
                                                bd=ad
                                                bd[k]=[]
                                                bv=av
                                                bv[k]=[]
                                                for count3 in range(target):
                                                    if self.Stop == True:
                                                        self.StopBoard()
                                                        break #counter 3                                                            
                                                    elif self.Pause == True:
                                                        self.PauseBoard()
                                                        for count_pause1 in range(target):
                                                            if self.Stop == True:
                                                                break #count_pause1
                                                            elif self.Resume == True:
                                                                self.ClockResume = clock
                                                                comment=[num2str(self.ClockResume(4)) , ':' , num2str(self.ClockResume(5)) ,':' ,num2str(self.ClockResume(6)), ' Interface resumed by the user.'] 
                                                                diary on
                                                                disp(comment)
                                                                diary off 
                                                                self.SPS01[0,b[0]].UpdateStatus() #############################
                                                                self.MulMove3[bd[1],bv[1]]                                  
                                                                self.flag_break_countpause = 1
                                                                break #count_pause1
                                                            time.sleep(scan_rate)                                                           
                                                    elif self.SPS01[0,b[0]].FlagIsMoving == True:
                                                        self.SPSO1[0,b[0]].UpdateStatus()
                                                    if self.flag_break_countpause == 1:
                                                        break #counter1  
                                                    elif self.SPS01[0,b[0]].FlagIsDone == True:
                                                        self.SPS01[0,b[0]].displaymovementstop()
                                                        break #counter 3
                                                    time.sleep(scan_rate)
                                                break # k search of first device to be done 
                                        break # counter 2                                      
                                    time.sleep(scan_rate)
                                break # j search of first device to be done 
                        break # counter 1
                    time.sleep(scan_rate)

      ## CONTINUE FROM 4 SYRINGES 
        pass
    ## TODO ##

    ## Multiple Movement with stop (at the same time. It allows the stop and pause)
    def MulMove3(self,d1,v1,d2,v2,d3,v3,d4,v4,d5,v5,d6,v6,d7,v7,d8,v8):
        pass
    ## TODO ##

    ## Display movement stopwait
    def displaymovementstopwait(self,t):
        pass
    ## TODO ##

    ## WaitStopBoard
    def WaitStopBoard(self):
        pass
    ## TODO ##

    ## Update
    def UpdateBoard(self):
        pass
    ## TODO ##

    ## Wait Movement
    def MoveWait(self,time,d1,v1,d2,v2,d3,v3,d4,v4,d5,v5,d6,v6,d7,v7,d8,v8):
        pass
    ## TODO ##

    ## Listener Function : Display the first device to be done and Stop and Pause and chech the WAIT (called in MoveWait)
    def CheckFirstDoneStopPauseWait(self,args):
        pass
    ## TODO ##

    ## Set Valves2 It allows the pause too
    def SetValves2(self,d1,v11,v12,v13,v14,d2,v21,v22,v23,v24):
        pass
    ## TODO ##

    ## Check First Done Stop Pause M
    def CheckFirstDoneStopPauseM(self,args):
        pass
    ## TODO ##
