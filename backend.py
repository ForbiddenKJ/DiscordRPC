## Import

from pypresence import Presence
import multiprocessing as mp
import psutil
import time

## Main Class

class discordrpc:
    def __init__(self):
        self.activeProcess = []

    def connect(self, C_ID : str):
        self.C_ID = C_ID
        self.RPC = Presence(self.C_ID,pipe=0)
        self.RPC.connect()

    def updateVariables(self, C_ID, state, details, large_image = None, small_image = None):
        self.C_ID = C_ID
        self.state = state
        self.details = details
        self.large_image = large_image
        self.small_image = small_image

        if self.large_image == '': self.large_image = None
        if self.small_image == '': self.small_image = None

    def updateStatus(self):
        if self.large_image is not None and self.small_image is not None:
            update = self.RPC.update(state=self.state,
                                details=self.details,
                                large_image=self.large_image,
                                small_image=self.small_image)

        if self.small_image is None:
            update = self.RPC.update(state=self.state,
                                details=self.details,
                                large_image=self.large_image)

        if self.large_image is None:
            update = self.RPC.update(state=self.state,
                                details=self.details)

    def stopConnection(self):
        kills = 0
        for x, i in enumerate(self.activeProcess):
            i.kill()
            del self.activeProcess[x]
            kills += 1

        self.RPC.clear()

        if kills > 1:
            print('WARNING: ',kills, 'Connection(s) Killed')

        def disconnect(self):
            # Clean Close

            self.stopConnection()

            # Close
            self.RPC.close()

    def _stayConnected(self):
        while True:
            self.updateStatus()
            time.sleep(15)

    def stayConnected(self):

        self.stopConnection()

        self.activeProcess.append(True)
        self.activeProcess[-1] = mp.Process(target=self._stayConnected, daemon=True)

        self.activeProcess[-1].start()

    def backProcess(self, C_ID, state, details, large_image = None, small_image = None):

        self.updateVariables(C_ID, state, details, large_image, small_image)
        self.stayConnected()

    # Presets

    # CPU & RAM Realtime Display

    def customRPC(self, function, C_ID : str, state : str, details : str, large_image : str = None, small_image : str = None):
        self.updateVariables(C_ID, state, details, large_image, small_image)

        self.stopConnection()

        self.activeProcess.append(True)
        self.activeProcess[-1] = mp.Process(target=function, daemon=True)

        self.activeProcess[-1].start()

    def realTimeCPUUpdateLoop(self):
        template = self.state

        while True:
            cpu = round(psutil.cpu_percent(),1)
            mem = round(psutil.virtual_memory().percent,1)
            self.state = template.replace('[CPU]', str(cpu)).replace('[RAM]', str(mem))

            self.updateStatus()

            time.sleep(15)

    # Epoch Realtime Display

    def realTimeEpochUpdateLoop(self):
        template = 'Epoch [EPOCH]'

        while True:
            epoch = time.time()
            self.state = template.replace('[EPOCH]', str(epoch))

            self.updateStatus()

            time.sleep(15)
