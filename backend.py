from pypresence import Presence
import threading
import time


class discordrpc:
    def __init__(self, C_ID : str, state : str, details : str, large_image : str = None, small_image : str = None):
        self.C_ID = C_ID
        self.state = state
        self.details = details
        self.large_image = large_image
        self.small_image = small_image
        self.doConnection = True
        self.RPC = None

        if self.large_image == '': self.large_image = None
        if self.small_image == '': self.small_image = None

    def switch(self) -> bool:
        self.doConnection = not self.doConnection
        return self.doConnection

    def flickSwitch(self):
        self.switch()
        self.switch()

    def connect(self) -> bool:
        #try:
        self.RPC = Presence(self.C_ID,pipe=0)
        self.RPC.connect()

        return True

        # TODO: Add specific error checks
        #except:
            #return False

    def updateStatus(self) -> bool:
        # try:
        if self.large_image is not None and self.small_image is not None:
            update = self.RPC.update(state=self.state,
                                details=self.details,
                                large_image=self.large_image,
                                small_image=self.small_image)

        elif self.small_image is None:
            update = self.RPC.update(state=self.state,
                                details=self.details,
                                large_image=self.large_image)

        elif self.large_image is None:
            update = self.RPC.update(state=self.state,
                                details=self.details)

        return True


        # TODO: Add specific error checks
        # except:
        #     return False

    def _stayConnected(self):
        while self.doConnection:
            time.sleep(15)

    def stayConnected(self):
        self.threaded = threading.Thread(target=self._stayConnected)
        self.threaded.daemon = True
        self.threaded.start()

        return
        # self.threaded.join()
