import os
import subprocess
import platform
from pathlib import Path

from .tasks import Task

from typing import Union


class OpenOrStart:
    """Same as double clicking on a file"""
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __call__(self, _: Task):
        system = platform.system()
        if system == 'Windows':
            # MyPy reports this as invalid since it's not available on Linux
            os.startfile(self.path)  # type: ignore
        elif system == 'Linux':
            subprocess.call(['xdg-open', str(self.path)],
                            close_fds=True, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        elif system == 'Darwin':
            subprocess.call(['open', str(self.path)],
                            close_fds=True, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        else:
            raise RuntimeError(f"Unsupported platform: {platform.system}.")
