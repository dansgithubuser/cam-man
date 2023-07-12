import shutil
import time

class Disk:
    def __init__(self, rm_list, min_free_gb=1, rm_amount_gb=0.1):
        self.rm_list = rm_list
        self.min_free_gb = min_free_gb
        self.rm_amount_gb = rm_amount_gb
        self.last_check_at = time.time()

    def update(self):
        now = time.time()
        if now - self.last_check_at < 60:
            return
        self.last_check_at = now
        if shutil.disk_usage('.').free / 1e9 > self.rm_thresh_gb:
            return
        for path in self.rm_list():
            os.remove(path)
            if shutil.disk_usage('.').free / 1e9 > self.rm_thresh_gb + self.rm_amount_gb:
                break
