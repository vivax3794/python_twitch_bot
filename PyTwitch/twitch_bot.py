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

    def _import_cog(self, current_object, import_paths: List[None]):
        if len(import_paths) == 0:
            return current_object

        attr = import_paths.pop(0)
        current_object = getattr(current_object, attr)
        return self._import_cog(current_object, import_paths)

    def load_cog(self, cog_name: str) -> None:
        """
        Load a cog.

        The cog_name is the path to the file, so if I has a cog in cogs/info.py
        I would set cog_name to "cogs.info"

        Once a cog is loaded, it get's it's setup function run.
        here is a example of a cog:

        def setup(bot):
            @bot.command()
            def test(ctx):
                ctx.reply("Hello World!")
        """
        cog = __import__(cog_name)
        import_path = cog_name.split(".")[1:]
        cog = self._import_cog(cog, import_path)
        cog.setup(self)

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
