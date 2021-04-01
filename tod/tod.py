from prompt_toolkit import Application
from prompt_toolkit.layout import (Layout, ConditionalContainer,
                                   FloatContainer, Float)
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.widgets import Label, Dialog, Button

from prompt_toolkit.layout.containers import HSplit

from prompt_toolkit.filters import Condition

from .tasks import Task, TaskAction
from .actions import OpenOrStart

from typing import Optional, List, Callable


placeholder = Task('No tasks yet...', '', 'grey')


class NoActionDialog(ConditionalContainer):
    def __init__(self, ok_btn_cb: Callable[[], None] = None):
        if ok_btn_cb is None:
            ok_btn_cb = self.hide

        self.dialog = Dialog(
            body=Label("Task has no action associated"),
            title="🙄",
            buttons=[Button("Ok", handler=ok_btn_cb)],
            modal=True
        )
        self.visible = False

        super().__init__(self.dialog, filter=Condition(lambda: self.visible))

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True


class TaskList(HSplit):
    def __init__(self, tasks: Optional[List[Task]] = None, wrap=True,
                 default_action: TaskAction = lambda t: None):
        if tasks is None:
            tasks = [placeholder]

        self._cards = [TaskCard(task, default_action) for task in tasks]

        self._selected_idx = 0
        self._cards[self._selected_idx].selected = True

        self.wrap = wrap

        super().__init__(self._cards)

    @property
    def selected_card(self):
        return self._cards[self.selected_idx]

    @property
    def selected_idx(self):
        return self._selected_idx

    @selected_idx.setter
    def selected_idx(self, idx: int):
        assert 0 <= idx < len(self._cards)
        self._cards[self._selected_idx].selected = False
        self._selected_idx = idx
        self._cards[self._selected_idx].selected = True

    def next(self):
        if self.selected_idx == len(self._cards) - 1:
            if self.wrap:
                self.selected_idx = 0
            else:
                return
        else:
            self.selected_idx += 1

    def prev(self):
        if self.selected_idx == 0:
            if self.wrap:
                self.selected_idx = len(self._cards) - 1
            else:
                return
        else:
            self.selected_idx -= 1


HR_BAR = ('grey', '—' * 20)


class TaskCard(Label):
    def __init__(self, task, default_action: TaskAction):
        self.selected = False
        self._default_action = default_action
        self._task = task
        self._summary_style = (
            f"{self._task.color} {'bold' if self.selected else ''}"
        )
        super().__init__(self.contents)

    def contents(self):
        return self._multiline() if self.selected else self._oneline()

    def _oneline(self):
        return FormattedText([
            (self._summary_style, f"   {self._task.summary}"),
        ])

    def _multiline(self):
        return FormattedText([
            (self._summary_style, f" ▷ {self._task.summary}"),
            ('', f"\n\n{self._task.description}\n"),
            HR_BAR
        ])

    def run_action(self):
        if self._task.action is None:
            return self._default_action(self._task)
        return self._task.action(self._task)


class TUI(Application):
    def __init__(self):
        self.no_action_dialog = NoActionDialog(
            ok_btn_cb=self.kb_run_action_or_dismiss
        )
        self.key_bindings = self._init_keybindings()

        tasks = [
            Task('task1, summary', "Longer description", "lightblue",
                 action=OpenOrStart('https://github.com/')),
            Task('task2, summary', "Longer description", "orange"),
            Task('task3, summary', "Longer description", "lightgreen"),
            Task('task4, summary', "Longer description", "darkred"),
            Task('task5, summary', "Longer description", "gray"),
            Task('task6, summary', "Longer description", "darkmagenta"),
        ]
        self.tasklist = TaskList(
            tasks, default_action=lambda t: self.no_action_dialog.show()
        )

        layout = Layout(
            FloatContainer(
                content=self.tasklist,
                floats=[Float(self.no_action_dialog)]
            )
        )

        style = Style([])

        super().__init__(
            layout, style, key_bindings=self.key_bindings, full_screen=True
        )

    def _init_keybindings(self):
        key_bindings = KeyBindings()

        key_bindings.add('q')(self.kb_exit_gracefully)
        key_bindings.add('escape')(self.kb_exit_gracefully)
        key_bindings.add('enter')(self.kb_run_action_or_dismiss)
        key_bindings.add('a')(self.kb_run_action_or_dismiss)

        key_bindings.add('c-d')(self.kb_exit_gracefully)
        key_bindings.add('c-c')(self.kb_exit_gracefully)

        key_bindings.add('f12')(self.kb_debug)

        key_bindings.add('up')(self.kb_item_up)
        key_bindings.add('k')(self.kb_item_up)
        key_bindings.add('down')(self.kb_item_down)
        key_bindings.add('j')(self.kb_item_down)

        return key_bindings

    def kb_exit_gracefully(self, _):
        self.exit(0)

    def kb_debug(self, _):
        breakpoint()

    def kb_item_up(self, _):
        self.tasklist.prev()

    def kb_item_down(self, _):
        self.tasklist.next()

    def kb_run_action_or_dismiss(self, _=None):
        if self.no_action_dialog.visible:
            self.no_action_dialog.hide()
        else:
            self.tasklist.selected_card.run_action()
