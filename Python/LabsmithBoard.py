class LabsmithBoard:    
    
    ### i think init is equivalent to properties
    def __init__(self):
        ## General info
        self.MaxNumDev = []
        self.TotNumDev = [] 
        self.eib = [] 
        self.C4VM = [] 
        self.SPS01 = [] 
        
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
        ## TODO ##
        
        
        ## Listener
        # TODO ##
    


    ### Events
    ## TODO ###

    
    ### Constructor
    ## TODO ##

    ### Destructor
    ## TODO ##

    ### Load
    def load(self):
        pass
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
                i1=FindIndexS(self,d1) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1))   # #it listens for the syringe FlagIsMoving == True, so it updtades continuously the state to determine the end of the command. It results in FlagReady = True again.
                if len(i1)>0:
                    if self.SPS01[1,i1].FlagIsDone == True:
                        self.SPS01[1,i1].device.CmdMoveToVolume(v1)                             
                        self.SPS01[1,i1].FlagReady = False 
                        displaymovement(self.SPS01[1,i1])
                        if self.SPS01[1,i1].FlagIsMoving == True:
                            notify(self.SPS01[1,i1],'MovingState') 
            elif v2 != None and d3 == None:  # # 2 syringes as input
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2)  
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0:
                    if self.SPS01[1,i1].FlagIsDone == True and self.SPS01[1,i2].FlagIsDone == True:
                        self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                        self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                        self.SPS01[1,i1].FlagReady = False 
                        self.SPS01[1,i2].FlagReady = False 
                        displaymovement(self.SPS01[1,i1])
                        displaymovement(self.SPS01[1,i2])  
                        if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True:
                            notify(self,'FirstDone') 

            elif v3 != None and d4 == None:  # # 3 syringes as input
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2) 
                i3=FindIndexS(self,d3) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2,i3))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0:
                    self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[1,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[1,i1].FlagReady = False 
                    self.SPS01[1,i2].FlagReady = False 
                    self.SPS01[1,i3].FlagReady = False 
                    displaymovement(self.SPS01[1,i1])
                    displaymovement(self.SPS01[1,i2]) 
                    displaymovement(self.SPS01[1,i3])
                    if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True and self.SPS01[1,i3].FlagIsMoving == True:
                        notify(self,'FirstDone') 
                    end
                end                    
            elif v4 != None and d5 == None  # # 4 syringes as input:
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2) 
                i3=FindIndexS(self,d3) 
                i4=FindIndexS(self,d4) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2,i3,i4))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0:
                    self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[1,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[1,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[1,i1].FlagReady = False 
                    self.SPS01[1,i2].FlagReady = False 
                    self.SPS01[1,i3].FlagReady = False 
                    self.SPS01[1,i4].FlagReady = False 
                    displaymovement(self.SPS01[1,i1])
                    displaymovement(self.SPS01[1,i2]) 
                    displaymovement(self.SPS01[1,i3])
                    displaymovement(self.SPS01[1,i4])
                    if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True and self.SPS01[1,i3].FlagIsMoving == True and self.SPS01[1,i4].FlagIsMoving == True
                        notify(self,'FirstDone') 
            elif v5 != None and d6 == None:  # # 5 syringes as input
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2) 
                i3=FindIndexS(self,d3) 
                i4=FindIndexS(self,d4) 
                i5=FindIndexS(self,d5) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2,i3,i4,i5))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0:
                    self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[1,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[1,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[1,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[1,i1].FlagReady = False 
                    self.SPS01[1,i2].FlagReady = False 
                    self.SPS01[1,i3].FlagReady = False 
                    self.SPS01[1,i4].FlagReady = False 
                    self.SPS01[1,i5].FlagReady = False 
                    displaymovement(self.SPS01[1,i1])
                    displaymovement(self.SPS01[1,i2]) 
                    displaymovement(self.SPS01[1,i3])
                    displaymovement(self.SPS01[1,i4])
                    displaymovement(self.SPS01[1,i5])
                    if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True and self.SPS01[1,i3].FlagIsMoving == True and self.SPS01[1,i4].FlagIsMoving == True and self.SPS01[1,i5].FlagIsMoving == True:
                        notify(self,'FirstDone') 
            elif v6 != None and d7 == None:  # # 6 syringes as input
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2) 
                i3=FindIndexS(self,d3) 
                i4=FindIndexS(self,d4) 
                i5=FindIndexS(self,d5) 
                i6=FindIndexS(self,d6) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2,i3,i4,i5,i6))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0 and len(i6)>0:
                    self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[1,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[1,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[1,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[1,i6].device.CmdMoveToVolume(v6) 
                    self.SPS01[1,i1].FlagReady = False 
                    self.SPS01[1,i2].FlagReady = False 
                    self.SPS01[1,i3].FlagReady = False 
                    self.SPS01[1,i4].FlagReady = False 
                    self.SPS01[1,i5].FlagReady = False 
                    self.SPS01[1,i6].FlagReady = False 
                    displaymovement(self.SPS01[1,i1])
                    displaymovement(self.SPS01[1,i2]) 
                    displaymovement(self.SPS01[1,i3])
                    displaymovement(self.SPS01[1,i4])
                    displaymovement(self.SPS01[1,i5])
                    displaymovement(self.SPS01[1,i6])
                    if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True and self.SPS01[1,i3].FlagIsMoving == True and self.SPS01[1,i4].FlagIsMoving == True and self.SPS01[1,i5].FlagIsMoving == True and self.SPS01[1,i6].FlagIsMoving == True:
                        notify(self,'FirstDone') 
            elif v7 != None and d8 == None:  # # 7 syringes as input
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2) 
                i3=FindIndexS(self,d3) 
                i4=FindIndexS(self,d4) 
                i5=FindIndexS(self,d5) 
                i6=FindIndexS(self,d6) 
                i7=FindIndexS(self,d7) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2,i3,i4,i5,i6,i7))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0 and len(i6)>0 and len(i7)>0:
                    self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[1,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[1,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[1,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[1,i6].device.CmdMoveToVolume(v6) 
                    self.SPS01[1,i7].device.CmdMoveToVolume(v7) 
                    self.SPS01[1,i1].FlagReady = False 
                    self.SPS01[1,i2].FlagReady = False 
                    self.SPS01[1,i3].FlagReady = False 
                    self.SPS01[1,i4].FlagReady = False 
                    self.SPS01[1,i5].FlagReady = False 
                    self.SPS01[1,i6].FlagReady = False 
                    self.SPS01[1,i7].FlagReady = False 
                    displaymovement(self.SPS01[1,i1])
                    displaymovement(self.SPS01[1,i2]) 
                    displaymovement(self.SPS01[1,i3])
                    displaymovement(self.SPS01[1,i4])
                    displaymovement(self.SPS01[1,i5])
                    displaymovement(self.SPS01[1,i6])
                    displaymovement(self.SPS01[1,i7])
                    if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True and self.SPS01[1,i3].FlagIsMoving == True and self.SPS01[1,i4].FlagIsMoving == True and self.SPS01[1,i5].FlagIsMoving == True and self.SPS01[1,i6].FlagIsMoving == True and self.SPS01[1,i7].FlagIsMoving == True:
                        notify(self,'FirstDone') 
            elif v8 != None:  # # 8 syringes as input
                i1=FindIndexS(self,d1) 
                i2=FindIndexS(self,d2) 
                i3=FindIndexS(self,d3) 
                i4=FindIndexS(self,d4) 
                i5=FindIndexS(self,d5) 
                i6=FindIndexS(self,d6) 
                i7=FindIndexS(self,d7) 
                i8=FindIndexS(self,d8) 
                self.listener_firstdone = addlistener(self, 'FirstDone',@(src,evnt)self.CheckFirstDone(src,evnt,i1,i2,i3,i4,i5,i6,i7,i8))   # #it listens for the syringes FlagIsMoving == True, so it updtades continuously the states to determine the end of the commands. It results in FlagReady = True again.
                if len(i1)>0 and len(i2)>0 and len(i3)>0 and len(i4)>0 and len(i5)>0 and len(i6)>0 and len(i7)>0 and len(i8)>0:
                    self.SPS01[1,i1].device.CmdMoveToVolume(v1) 
                    self.SPS01[1,i2].device.CmdMoveToVolume(v2) 
                    self.SPS01[1,i3].device.CmdMoveToVolume(v3) 
                    self.SPS01[1,i4].device.CmdMoveToVolume(v4) 
                    self.SPS01[1,i5].device.CmdMoveToVolume(v5) 
                    self.SPS01[1,i6].device.CmdMoveToVolume(v6) 
                    self.SPS01[1,i7].device.CmdMoveToVolume(v7) 
                    self.SPS01[1,i8].device.CmdMoveToVolume(v8) 
                    self.SPS01[1,i1].FlagReady = False 
                    self.SPS01[1,i2].FlagReady = False 
                    self.SPS01[1,i3].FlagReady = False 
                    self.SPS01[1,i4].FlagReady = False 
                    self.SPS01[1,i5].FlagReady = False 
                    self.SPS01[1,i6].FlagReady = False 
                    self.SPS01[1,i7].FlagReady = False 
                    self.SPS01[1,i8].FlagReady = False 
                    displaymovement(self.SPS01[1,i1])
                    displaymovement(self.SPS01[1,i2]) 
                    displaymovement(self.SPS01[1,i3])
                    displaymovement(self.SPS01[1,i4])
                    displaymovement(self.SPS01[1,i5])
                    displaymovement(self.SPS01[1,i6])
                    displaymovement(self.SPS01[1,i7])
                    displaymovement(self.SPS01[1,i8])
                    if self.SPS01[1,i1].FlagIsMoving == True and self.SPS01[1,i2].FlagIsMoving == True and self.SPS01[1,i3].FlagIsMoving == True and self.SPS01[1,i4].FlagIsMoving == True and self.SPS01[1,i5].FlagIsMoving == True and self.SPS01[1,i6].FlagIsMoving == True and self.SPS01[1,i7].FlagIsMoving == True and self.SPS01[1,i8].FlagIsMoving == True:
                        notify(self,'FirstDone')
            else:
                print('Error, missing input. Number of inputs has to be odd (interface, name of syringes and corresponding flow rates).')

        



            