from pypresence import Presence
import multiprocessing as mp

import time



class discordrpc:
    def __init__(self):
        self.activeProcess = []

    def connect(self, C_ID : str) -> bool:
        self.C_ID = C_ID
        self.RPC = Presence(self.C_ID,pipe=0)
        self.RPC.connect()

        return True

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

        if kills > 1:
            print('WARNING: ',kills, 'Connection(s) Killed')

    def _stayConnected(self):
        while True:
            self.updateStatus()
            time.sleep(15)

        return

    def stayConnected(self):

        self.stopConnection()

        self.activeProcess.append(True)
        self.activeProcess[-1] = mp.Process(target=self._stayConnected, daemon=True)

<<<<<<< HEAD
        #self.process.daemon = True
=======
>>>>>>> e758b9501896bd9a5ca10c298418f6e8148fd7df
        self.activeProcess[-1].start()

        return

    def backProcess(self, C_ID, state, details, large_image = None, small_image = None):

        self.updateVariables(C_ID, state, details, large_image, small_image)
        self.stayConnected()
