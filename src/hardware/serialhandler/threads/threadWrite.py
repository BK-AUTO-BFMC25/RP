# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
import threading
from multiprocessing import Pipe
from src.hardware.serialhandler.threads.messageconverter    import MessageConverter
from src.templates.threadwithstop import ThreadWithStop

class threadWrite(ThreadWithStop):
    # ===================================== INIT =========================================
    def __init__(self, queues, serialCom, logFile):
        super(threadWrite,self).__init__()
        self.queuesList       =  queues
        self.serialCom  =  serialCom
        self.logFile    =  logFile
        self.messageConverter = MessageConverter()
        self.running = False
        pipeRecvBreak, pipeSendBreak = Pipe(duplex=False)
        self.pipeRecvBreak= pipeRecvBreak
        self.queuesList["Config"].put({'Subscribe/Unsubscribe':1,"Owner": "PC", "msgID":5,"To":{"receiver": "processSerialHandler","pipe":pipeSendBreak}})
        pipeRecvSpeed, pipeSendSpeed = Pipe(duplex=False)
        self.pipeRecvSpeed= pipeRecvSpeed
        self.queuesList["Config"].put({'Subscribe/Unsubscribe':1,"Owner": "PC", "msgID":2,"To":{"receiver": "processSerialHandler","pipe":pipeSendSpeed}})
        pipeRecvSteer, pipeSendSteer = Pipe(duplex=False)
        self.pipeRecvSteer = pipeRecvSteer
        self.queuesList["Config"].put({'Subscribe/Unsubscribe':1,"Owner": "PC", "msgID":3,"To":{"receiver": "processSerialHandler","pipe":pipeSendSteer}})
        pipeRecvControl, pipeSendControl = Pipe(duplex=False)
        self.pipeRecvControl= pipeRecvControl
        self.queuesList["Config"].put({'Subscribe/Unsubscribe':1,"Owner": "PC", "msgID":4,"To":{"receiver": "processSerialHandler","pipe":pipeSendControl}})
        pipeRecvRunningSignal, pipeSendRunningSignal= Pipe(duplex = False )
        self.pipeRecvRunningSignal= pipeRecvRunningSignal
        self.queuesList["Config"].put({'Subscribe/Unsubscribe':1,"Owner": "PC", "msgID":1,"To":{"receiver": "processSerialHandler","pipe":pipeSendRunningSignal}})
        self.Queue_Sending()

    # ==================================== SENDING =======================================
    def Queue_Sending(self):
        self.queuesList["General"].put({ "Owner" : "processSerialHandler" , "msgID": 2, "msgType" :"Boolean2","msgValue":self.running})
        threading.Timer(1, self.Queue_Sending).start()

    # ===================================== RUN ==========================================
    def run(self):
        while self._running:
            try:
                if self.pipeRecvRunningSignal.poll():
                    msg= self.pipeRecvRunningSignal.recv()
                    if msg["value"] == True:
                        self.running = True
                    else:
                        self.running = False
                        command = {"action": "1" , "speed" : 0.0}  
                        command_msg = self.messageConverter.get_command(**command)
                        self.serialCom.write(command_msg.encode('ascii'))
                        self.logFile.write(command_msg) 
                        command = {"action": "2" , "steerAngle" : 0.0} 
                        command_msg = self.messageConverter.get_command(**command)
                        self.serialCom.write(command_msg.encode('ascii'))
                        self.logFile.write(command_msg)  
                if self.running:
                    if self.pipeRecvBreak.poll():
                        message = self.pipeRecvBreak.recv()
                        command = {"action": "1" , "speed" : float(message["value"])}
                        command_msg = self.messageConverter.get_command(**command)
                        self.serialCom.write(command_msg.encode('ascii'))
                        self.logFile.write(command_msg)
                    elif self.pipeRecvSpeed.poll():
                        message = self.pipeRecvSpeed.recv()
                        command = {"action": "1" , "speed" : float(message["value"])}
                        command_msg = self.messageConverter.get_command(**command)
                        self.serialCom.write(command_msg.encode('ascii'))
                        self.logFile.write(command_msg)
                    elif self.pipeRecvSteer.poll():
                        message = self.pipeRecvSteer.recv()
                        command = {"action": "2" , "steerAngle" : float(message["value"])}
                        command_msg = self.messageConverter.get_command(**command)
                        self.serialCom.write(command_msg.encode('ascii'))
                        self.logFile.write(command_msg)
            except Exception as e: 
                print(e) 
    # ==================================== START =========================================
    def start(self):
        super(threadWrite,self).start()
    # ==================================== STOP ==========================================
    def stop(self):
        super(threadWrite,self).stop()