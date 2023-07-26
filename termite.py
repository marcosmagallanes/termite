import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Input, TextLog, Header
from textual.reactive import reactive
from textual import log
from textual.validation import ValidationResult, Validator

from dotenv import load_dotenv
load_dotenv()

import openai

class InputValidator(Validator):
    """Validate input."""
    def validate(self, value: str) -> ValidationResult:
        def is_valid(value: str) -> bool:
            return len(value) > 0
        return self.success() if is_valid(value) else self.failure("No input!")

class TermiteChatApplication(App):
    """Main application."""

    messages = reactive([{'role': 'system', 'content':'You are Termite, a terminal based AI assistant.'}])

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TextLog(wrap=True, markup=True)
        yield Input(placeholder="Start typing...")

    def on_ready(self) -> None:
        """Handle application startup."""
        conversation_log = self.query_one(TextLog)

        for message in self.messages:
            conversation_log.write(f'{message["role"]}: {message["content"]}')

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted event."""

        if InputValidator().validate(event.input.value).is_valid:
            self.add_message('user', event.input.value)
            event.input.value = ''
        
        asyncio.create_task(self.send_request())
        
            
    def add_message(self, role, content):
        """Add to messages array and write to log."""

        # Add to self.messages array
        entry = {'role': role, 'content': content}
        self.messages.append(entry)

        # Write to self.TextLog
        conversation_log = self.query_one(TextLog)
        conversation_log.write(f'{entry["role"]}: {entry["content"]}')

    async def send_request(self):
        """Sends a request to the OpenAI chat API."""
        messages = self.messages
        log(f"Sending request with messages: {messages}")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        log(f"Received response: {response}")
        self.add_message('assistant', response.choices[0].message.content)
        log(self.messages)

if __name__ == "__main__":
    app = TermiteChatApplication()
    app.run()
