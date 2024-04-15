from .utils import invoke

from pathlib import Path
import re

def udevadm_find_cam():
    for path in Path('/dev').glob('video*'):
        out = invoke(f'udevadm info {path}', get_out=True)
        if re.search('ID_V4L_CAPABILITIES.*:capture:', out):
            index = int(re.search('(\d+)$', str(path)).group(1))
            return index, path
