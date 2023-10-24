"""
Python Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic librairy for create CLI in Pyth
on.

:copyright: Copyright (c) 2023 Overdjoker048
:license: MIT, see LICENSE for more details.

Create basic Python CLI::

    >>> import PyCLI
    >>> cli = PyCLI.CLI()
    >>> @cli.command()
    >>> def hello_world():
    >>>     print("Hello World")
    >>> cli.run()
"""

__encoding__ = "UTF-8"
__title__ = 'PyCLI'
__author__ = 'Overdjoker048'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023 Overdjoker048'
__version__ = '1.0'
__all__ = ['CLI', 'echo', 'prompt', 'write_logs']

import time
import inspect
from datetime import datetime
import os

class CLI:
    def __init__(self,
                 prompt: str = "Python@CLI\>",
                 not_exist: str = "This command does not exist.\nDo help to get the list of existing commands.",
                 logs: bool = True,
                 animation: bool = True,
                 cooldown: float = 0.1,
                 help_cmd: bool = True
                 ) -> None:
        """
        This object allows the creation of the CLI. The prompt parameter defines the 
        text that will be displayed in the terminal to enter the command. The not_exist 
        parameter will define the text that is displayed when a command does not exist.
        The logs parameter allows you to choose whether or not you want everything 
        displayed in the terminal to be rewritten in the logs. The animation and 
        cooldown parameters will define the display of CLI messages. Finally there is the
        help_cmd parameter which allows you to choose whether or not you want the CLI's 
        default help command.
        To launch the CLI you must use the run method of the CLI object.

        Exemple usage::

            >>> import PyCLI
            >>> cli = PyCLI.CLI(prompt="Python@CLI\>", logs=True, animation=True, cooldown=15, help_cmd=True, not_exist="This command does not exist.\nDo help to get the list of existing commands.")
            >>> @cli.command()
            >>> def hello_world():
            >>>     print("Hello World")
            >>> cli.run()
        """
        self.cmd = []
        self.prompt = prompt
        self.not_exist = not_exist
        self.logs = logs
        self.animation = animation
        self.cooldown = cooldown
        if help_cmd:
            @self.command(alias=["?"])
            def help() -> None:
                """Displays info about terminal commands."""
                text = ""
                for i in self.cmd:
                    if i["description"] is not None:
                        description = i["description"]
                    else:
                        description = ""
                    text += "Alias    "+ ", ".join(i["alias"])+" -> "+i["name"]+" "+" ".join(map(str, i["args"]))+f" {description}\n"
                echo(text[:-1], animation=self.animation, cooldown=self.cooldown, logs=self.logs)

        @self.command(alias=["exit"])
        def leave() -> None:
            """Close the terminal."""
            os.kill(os.getpid(), 9)

    def command(self,
                name: str = None,
                description: str = None,
                alias : list = []
                ) -> callable:
        """
        The command decorator allows you to define a function as a command for the CLI. You 
        can enter the name and/or description in the name and description parameters. If you
        don't, the command name will be the same name as the function. And for the description
        you can put it in doc form for your functions.

        Exemples usages::

            >>> import PyCLI
            >>> cli = PyCLI.CLI()
            >>> @cli.command(name="Hello World", description="This command write hello world in the terminal.")
            >>> def display_hello_world():
            >>>     print("Hello World")
            >>> cli.run()

            >>> import PyCLI
            >>> cli = PyCLI.CLI()
            >>> @cli.command()
            >>> def hello_world():
                    "This command write hello world in the terminal."
            >>>     print("Hello World")
            >>> cli.run()
        """
        def decorator(func: callable) -> callable:
            def wrapper(name:str, 
                        description: str, 
                        alias: list) -> None:
                name = name.replace(" ", "_").lower()
                types = []
                args = []
                for arg in inspect.signature(func).parameters.items():
                    types.append(str(arg[1].annotation))
                    args.append(f"[{arg[0]}]")

                cmd_info = {
                    "name": name,
                    "description": description,
                    "function": func,
                    "args": args,
                    "types": types,
                    "alias": alias,
                }
                self.cmd.append(cmd_info)
            return wrapper(name=name if name else func.__name__, 
                           description=description if description else func.__doc__, 
                           alias=alias)
        return decorator

    def run(self) -> None:
        """This method of the CLI object allows you to launch the CLI after you have created all your commands."""
        while True:
            try:
                self.cmd = sorted(self.cmd, key=lambda x: x["name"])
                entry = prompt(self.prompt, animation=self.animation, cooldown=self.cooldown, logs=self.logs).lower()
                exist = False
                for i in self.cmd:
                    if i["name"] == entry.split(" ")[0] or entry.split(" ")[0] in i["alias"]:
                        exist = True
                        args = []
                        for nmb, arg in enumerate(entry.split(" ")[1:len(i["args"])+1]):
                            match i["types"][nmb]:
                                case "<class 'int'>": args.append(int(arg))
                                case "<class 'bytes'>": args.append(arg.encode())
                                case "<class 'float'>": args.append(float(arg))
                                case "<class 'bool'>": args.append(bool(arg))
                                case _: args.append(arg)
                        i["function"](*args)
                if not exist:
                    echo(self.not_exist, animation=self.animation, cooldown=self.cooldown, logs=self.logs)
            except KeyboardInterrupt:
                continue
            except Exception as e:
                print(e)
                continue
            print()

def echo(*values: object,
         sep: str = " ",
         end: str = "\n",
         animation: bool = True,
         cooldown: float = 0.1,
         logs: bool = True
         ) -> None:
    """
    The echo method works like the print method which is already implemented in python but has a progressive 
    display system if the value of the animation parameter is set to True and also has a logging system that 
    writes the text you enter to the daily logs which is by default enabled. The cooldown parameter corresponds
    to the exposure time before displaying the next character (in MS) of the text you have entered if the 
    animation parameter is set to True.
    

    Exemple usage::

        >>> import PyCLI
        >>> PyCLI.echo("Hello World", animation=True, cooldown=15, logs=True, end="\n", sep=" ")
    """
    output = sep.join(map(str, values))
    for line in output.split("\n"):
        if animation:
            text = ""
            for i in line:
                text += i
                print(text, end="\r")
                time.sleep(cooldown / 1000)
        print(line, end=end)
    if logs:
        write_logs(output)


def prompt(__prompt: object = "",
           animation: bool = True,
           cooldown: int = 5,
           logs: bool = True
           ) -> str:
    """
    The prompt method works like the input method which is already implemented in python but has a progressive display 
    system if the value of the animation parameter is set to True and also includes a logging system that writes the 
    text that the user will respond to in the daily logs. The logging system is enabled by default. The cooldown 
    parameter corresponds to the exposure time before displaying the next character (in MS) of the text you have entered
    if the animation parameter is set to True.


    Exemple usage::

        >>> import PyCLI
        >>> PyCLI.prompt("What's your name ?", animation=True, cooldown=15, logs=True, end="\n", sep=" ")
    """
    for line in str(__prompt).split("\n"):
        if animation:
            text = ""
            for i in line:
                text += i
                print(text, end="\r")
                time.sleep(cooldown / 1000)
    returned = input(str(__prompt))
    if logs:
        write_logs(returned)
    return returned


def write_logs(*values: object,
               sep: str = " ",
               end: str = "\n",
               ) -> None:
    """
    The write_logs method allows to write in the daily logs. This method works like the print method which is already 
    implemented in python for the sep and end parameters.

    Exemple usage::

        >>> import PyCLI
        >>> PyCLI.write_logs("CLI was starting.")
    """
    text = sep.join(map(str, values)) + end
    if not os.path.exists("latest"):
        os.mkdir("latest")
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    time_now = f"{datetime.today().year}/{month[datetime.today().month - 1]}/{datetime.today().day} {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}"
    with open(f"latest/{datetime.today().date()}.log", "a", encoding="UTF-8") as file:
        file.write(f"[{time_now}] {text}")