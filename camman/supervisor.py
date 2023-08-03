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
                    break
                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise
                    traceback.print_exc()
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
