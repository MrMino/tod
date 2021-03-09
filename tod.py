from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.widgets import Label

from typing import Optional


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


class TUI(Application):
    def __init__(self):
        layout = Layout(
            Label(HTML("<placeholder>Placeholder</placeholder>"))
        )
        style = Style([
            ('placeholder', 'grey')
        ])
        key_bindings = KeyBindings()

        key_bindings.add('q')(self.kb_exit_gracefully)
        key_bindings.add('escape')(self.kb_exit_gracefully)
        key_bindings.add('c-d')(self.kb_exit_gracefully)
        key_bindings.add('c-c')(self.kb_exit_gracefully)

        super().__init__(
            layout, style, key_bindings=key_bindings, full_screen=True
        )

    def kb_exit_gracefully(self, _):
        self.exit(0)


TUI().run()
