from textual.app import App
from textual.widgets import Header

class ChatApp(App):

    def compose(self):
        yield Header()

if __name__ == "__main__":
    app = ChatApp()
    app.run()
