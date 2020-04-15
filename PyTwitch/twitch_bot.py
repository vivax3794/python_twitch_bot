import traceback
from typing import Callable, List, Dict, Optional

from .twitch_core import TwitchCore
from .utils import check_type
from .data_types import Message, Channel, User, Context, Command

class TwitchBot(TwitchCore):
    def __init__(self, prefix: str="!"):
        super().__init__()
        self.commands: Dict[str, Commands] = {}

        check_type("prefix", prefix, str)
        self.prefix = prefix

    def run(self) -> None:
        """
        Run the bots main loop.
        """
        while True:
            message = self.read_message()

            try:
                self.event_message(message)
            except Exception as e:
                self.event_error(e)

    def process_message(self, message: Message) -> None:
        """
        Check if the message is a command.

        If it is a command, fetch the command object and construct a ctx.
        """
        if message.content.startswith(self.prefix):
            command_name, *arguments = message.content[len(self.prefix):].split(" ")
            command = self.commands.get(command_name)
            if command is None:
                raise ValueError(f"Command {command_name} not found")

            ctx = Context(message)
            command.call(ctx, arguments)

    def command(self, command_name: Optional[str] = None) -> Callable[[Callable], None]:
        """
        Register a function as a command.
        """
        def Decorator(func: Callable) -> None:
            if command_name is None:
                inner_command_name = func.__name__
            else:
                inner_command_name = command_name

            command = Command(func)
            self.commands[inner_command_name] = command

        return Decorator

    def event_error(self, e):
        traceback.print_exc()

    def event_message(self, message: Message) -> None:
        print(f"{message.user.name}: {message.content}")
        self.process_message(message)
