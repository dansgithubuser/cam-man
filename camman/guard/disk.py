from pathlib import Path
import shutil
import time

class Disk:
    def __init__(self, rm_list, min_free_gb=1, rm_amount_gb=0.1):
        trial_rm_list = rm_list()
        if trial_rm_list:
            assert Path(trial_rm_list[0]).exists()
        self.rm_list = rm_list
        self.min_free_gb = min_free_gb
        self.rm_amount_gb = rm_amount_gb
        self.last_check_at = time.time()

    def update(self):
        now = time.time()
        if now - self.last_check_at < 60:
            return
        self.last_check_at = now
        if shutil.disk_usage('.').free / 1e9 > self.min_free_gb:
            return
        for path in self.rm_list():
            path = Path(path)
            if path.is_dir():
                if not next(path.iterdir(), False):
                    path.rmdir()
            else:
                path.unlink()
            if shutil.disk_usage('.').free / 1e9 > self.min_free_gb + self.rm_amount_gb:
                break
