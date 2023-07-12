import time
import traceback

class Supervisor:
    def __init__(self, f):
        self.f = f

    def run(self):
        while True:
            try:
                self.f()
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()
            time.sleep(1)
