import os
import subprocess
import platform
from pathlib import Path

from .tasks import Task, TaskAction

from typing import Union


class OpenOrStart(TaskAction):
    """Same as double clicking on a file"""
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __call__(self, _: Task):
        if platform.system == 'Windows':
            # MyPy reports this as invalid since it's not available on Linux
            os.startfile(self.path)  # type: ignore
        elif platform.system == 'Linux':
            subprocess.Popen(['xdg-open', str(self.path)], close_fds=True)
