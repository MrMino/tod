from dataclasses import dataclass

from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.widgets import Label

from prompt_toolkit.layout.containers import HSplit

from typing import Optional, List


class MutableRule:
    def __init__(self,
                 class_name: str,
                 color: Optional[str] = '',
                 bgcolor: Optional[str] = '',
                 bold: Optional[bool] = False,
                 underline: Optional[bool] = False,
                 italic: Optional[bool] = False,
                 blink: Optional[bool] = False,
                 reverse: Optional[bool] = False,
                 hidden: Optional[bool] = False):
        self._class_name = class_name
        self.color = color
        self.bgcolor = bgcolor
        self.bold = bold
        self.underline = underline
        self.italic = italic
        self.blink = blink
        self.reverse = reverse
        self.hidden = hidden

    @property
    def class_name(self):
        return self._class_name

    def __str__(self):
        return (self.color
                + (f' {self.bgcolor}' if self.bgcolor else '')
                + (' bold' if self.bold else '')
                + (' underline' if self.underline else '')
                + (' italic' if self.italic else '')
                + (' blink' if self.blink else '')
                + (' reverse' if self.reverse else '')
                + (' hidden' if self.hidden else ''))

    # Required for MutableStyle.invalidation_hash() to update.
    def __hash__(self):
        return id(str(self))

    def __iter__(self):
        return iter([self.class_name, str(self)])


class MutableStyle(Style):
    def invalidation_hash(self):
        return hash(tuple(self.style_rules))


@dataclass
class Task:
    summary: str
    description: str
    color: str


class TaskList(HSplit):
    def __init__(self, tasks: Optional[List[Task]], wrap=True):
        if tasks is None:
            tasks = []

        self._cards = [TaskCard(task) for task in tasks]

        self._selected = 0
        self._cards[self._selected].selected = True

        self.wrap = wrap

        super().__init__(self._cards)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, idx: int):
        assert 0 <= idx < len(self._cards)
        self._cards[self._selected].selected = False
        self._selected = idx
        self._cards[self._selected].selected = True

    def next(self):
        if self.selected == len(self._cards) - 1:
            if self.wrap:
                self.selected = 0
            else:
                return
        else:
            self.selected += 1

    def prev(self):
        if self.selected == 0:
            if self.wrap:
                self.selected = len(self._cards) - 1
            else:
                return
        else:
            self.selected -= 1


HR_BAR = ('grey', '—' * 20)


class TaskCard(Label):
    def __init__(self, task):
        self.selected = False
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


placeholder = Label(HTML("<placeholder>Placeholder</placeholder>"))
placeholder_style = MutableRule('placeholder', 'grey', bold=False)


class TUI(Application):
    def __init__(self):
        tasks = [
            Task('task1, summary', "Longer description", "lightblue"),
            Task('task2, summary', "Longer description", "orange"),
            Task('task3, summary', "Longer description", "lightgreen"),
            Task('task4, summary', "Longer description", "darkred"),
            Task('task5, summary', "Longer description", "gray"),
            Task('task6, summary', "Longer description", "magenta"),
        ]
        self.tasklist = TaskList(tasks)

        layout = Layout(
            self.tasklist
        )
        style = MutableStyle([
            placeholder_style,
        ])
        key_bindings = KeyBindings()

        key_bindings.add('q')(self.kb_exit_gracefully)
        key_bindings.add('escape')(self.kb_exit_gracefully)
        key_bindings.add('c-d')(self.kb_exit_gracefully)
        key_bindings.add('c-c')(self.kb_exit_gracefully)

        key_bindings.add('f12')(self.kb_debug)

        key_bindings.add('up')(self.kb_item_up)
        key_bindings.add('down')(self.kb_item_down)

        super().__init__(
            layout, style, key_bindings=key_bindings, full_screen=True
        )

    def kb_exit_gracefully(self, _):
        self.exit(0)

    def kb_debug(self, _):
        breakpoint()

    def kb_item_up(self, _):
        self.placeholder_style.bold = not self.placeholder_style.bold
        self.invalidate()

    def kb_item_down(self, _):
        pass


TUI().run()
