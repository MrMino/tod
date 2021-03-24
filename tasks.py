from dataclasses import dataclass

from typing import Optional, Callable, Any

TaskAction = Callable[['Task'], Any]


@dataclass
class Task:
    summary: str
    description: str
    color: str
    action: Optional[TaskAction] = None
