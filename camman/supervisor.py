import time
import traceback

class Supervisor:
    def __init__(self, f):
        self.f = f

    def run(self):
        try:
            while True:
                try:
                    self.f()
                except:
                    traceback.print_exc()
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
