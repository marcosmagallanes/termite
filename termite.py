from textual.app import App
from textual.containers import VerticalScroll
from textual.widgets import Input, Static, Placeholder, Label, Header, Footer
from textual.reactive import reactive

class TermiteChatApplication(App):
    def compose(self):
        yield Header()
        yield VerticalScroll()
        yield Input()
        yield Footer()

if __name__ == "__main__":
    app = TermiteChatApplication()
    app.run()
