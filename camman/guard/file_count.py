from pathlib import Path
import time

class FileCount:
    def __init__(self, rm_list, max_files=1000, period=3600):
        trial_rm_list = rm_list()
        if trial_rm_list:
            assert Path(trial_rm_list[0]).exists()
        self.rm_list = rm_list
        self.max_files = max_files
        self.period = period
        self.last_check_at = time.time()

    def update(self):
        now = time.time()
        if now - self.last_check_at < self.period:
            return
        self.last_check_at = now
        rm_list = self.rm_list()
        n_to_rm = len(rm_list) - self.max_files
        for path in rm_list:
            if n_to_rm <= 0: break
            path = Path(path)
            if path.is_dir():
                if not next(path.iterdir(), False):
                    path.rmdir()
                    n_to_rm -= 1
            else:
                path.unlink()
                n_to_rm -= 1
