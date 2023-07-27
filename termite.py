import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Input, TextLog, Header
from textual.reactive import reactive
from textual import log
from textual.validation import ValidationResult, Validator

from rich.console import Text

from dotenv import load_dotenv
load_dotenv()

import openai

class Termite(App):
    """Main application."""

    CSS_PATH = 'styles.css'
    messages = reactive([])

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TextLog(wrap=True, markup=True)
        yield Input(placeholder="Start typing...")

    def on_mount(self) -> None:
        """Handle application startup."""

        self.add_message('system', 'You are Termite, a terminal based AI assistant.')

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted event."""

        if InputValidator().validate(event.input.value).is_valid:
            self.add_message('user', event.input.value)
            event.input.value = ''
        
        asyncio.create_task(self.send_request())
        
            
    def add_message(self, role, content):
        """Add to messages array and write to log."""

        entry = {'role': role, 'content': content}
        self.messages = [*self.messages, entry]

    def watch_messages(self, old_messages: list, new_messages: list) -> None:
        """Handle messages change by writing to log."""

        diffs = [message for message in new_messages if message not in old_messages]

        text_log = self.query_one(TextLog)
        for message in diffs:
            text_log.write(
                Text(f'{message["role"]}: {message["content"]}')
                )
        

    async def send_request(self):
        """Sends a request to the OpenAI chat API."""

        messages = self.messages
        # log(f"Sending request with messages: {messages}")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        # log(f"Received response: {response}")
        self.add_message('assistant', response.choices[0].message.content)
        # log(self.messages)

class InputValidator(Validator):
    """Validate input."""
    def validate(self, value: str) -> ValidationResult:
        def is_valid(value: str) -> bool:
            return len(value) > 0
        return self.success() if is_valid(value) else self.failure("No input!")

if __name__ == "__main__":
    app = Termite()
    app.run()
