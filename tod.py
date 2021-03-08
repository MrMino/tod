from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.widgets import Label


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
