from multiprocessing import Process
import time
import traceback

class Backoff:
    def __init__(self):
        self.t = 1

    def duration(self):
        self.t = min(2 * self.t, 600)
        return self.t

backoff = Backoff()

class Supervisor:
    def __init__(self, f):
        self.f = f

    def run(self):
        try:
            while True:
                p = Process(target=self.f)
                p.start()
                p.join()
                time.sleep(backoff.duration())
        except KeyboardInterrupt:
            pass
