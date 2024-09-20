"""
Python Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic librairy for create CLI in Pyth
on.

:copyright: Copyright (c) 2023-2024 Overdjoker048
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
__copyright__ = 'Copyright (c) 2023-2024 Overdjoker048'
__version__ = '1.2.0'
__all__ = ['CLI', 'echo', 'prompt', 'write_logs', 'colored', 'gram']

import colorama
import inspect
from datetime import datetime
import os
import platform
import time
import sys
import shlex

colorama.init()
home = "\\".join(__file__.split("\\")[:-1])

class CLI:
    def __init__(self,
                 prompt: str | None = "[{}]@[{}]\\>",
                 user: str = "Python-Cli",
                 title: str | None = None,
                 logs: bool = True,
                 anim: bool = True,
                 cool: float | int = 0.1,
                 color: tuple | str | None = None,
                 help_cmd: bool = True,
                 not_exist: str = "{} doesn't exist.\nDo help to get the list of existing commands.",
                 unexpected: str = "An unexpected error occurred: {}"
                 ) -> None:
        """
        This object allows the creation of the CLI. The prompt parameter defines the 
        text that will be displayed in the terminal to enter the command. The not_exist 
        parameter will define the text that is displayed when a command does not exist.
        The logs parameter allows you to choose whether or not you want everything 
        displayed in the terminal to be rewritten in the logs. The anim and 
        cool parameters will define the display of CLI messages. Finally there is the
        help_cmd parameter which allows you to choose whether or not you want the CLI's 
        default help command.
        To launch the CLI you must use the run method of the CLI object.

        Example of use::

            >>> import PyCLI
            >>> cli = PyCLI.CLI(prompt="Python@CLI\\>", logs=True, anim=True, cool=15, help_cmd=True, not_exist="This command does not exist.\nDo help to get the list of existing commands.")
            >>> @cli.command()
            >>> def hello_world():
            >>>     print("Hello World")
            >>> cli.run()
        """
        if title is not None:
            match platform.system():
                case "Windows": os.system(f"title {title}")
                case "Linux" | "Darwin": os.system(f"echo -n '\033]0;{title}\007'")

        self.__cmd = {}
        self.prompt = prompt
        self.user = user
        self.path = home
        self.logs = logs
        self.anim = anim
        self.cool = cool
        self.color = color
        self.not_exist = not_exist
        self.unexpected = unexpected

        match platform.system():
            case "Windows": self.__clear_cmd = "cls"
            case "Linux" | "Darwin": self.__clear_cmd = "clear"

        if help_cmd:
            @self.command(alias=["?"], doc=self.help.__doc__)
            def help() -> None:
                self.help()
        else:
            del self.help

        @self.command(alias=["cd"], doc=self.change_directory.__doc__)
        def change_directory(path: str = home) -> None:
            self.change_directory(path)

        @self.command(alias=[self.__clear_cmd], name="clear-host", doc=self.clear_host.__doc__)
        def clear_host() -> None:
            self.clear_host()

        @self.command(alias=["exit"], doc=self.leave.__doc__)
        def leave() -> None:
            self.leave()

    def command(self,
                name: str = None,
                doc: str = None,
                alias : list = []
                ) -> callable:
        """
        The command decorator allows you to define a function as a command for the CLI. You 
        can enter the name and/or description in the name and doc parameters. If you
        don't, the command name will be the same name as the function. And for the description
        you can put it in doc form for your functions.

        Examples of use::

            >>> import PyCLI
            >>> cli = PyCLI.CLI()
            >>> @cli.command(name="Hello World", doc="This command write hello world in the terminal.")
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
                        doc: str, 
                        alias: list) -> None:
                name = name.replace(" ", "_").lower()
                types = []
                args = []

                for arg in inspect.signature(func).parameters.items():
                    types.append(arg[1].annotation)
                    args.append(f"[{arg[0]}]")
                self.__cmd[name] = {
                        "doc": doc,
                        "function": func,
                        "args": args,
                        "types": types,
                        "alias": alias,
                }
                for i in alias:
                    self.__cmd[i] = name
            return wrapper(name=name if name else func.__name__, 
                           doc=doc if doc else func.__doc__, 
                           alias=alias)
        return decorator

    def leave(self) -> None:
        "Close the terminal."
        os.kill(os.getpid(), 9)

    def clear_host(self) -> None:
        "Reset the display of the terminal."
        os.system(self.__clear_cmd)

    def help(self) -> None:
        "Displays info about terminal commands."
        text = ""
        for i in self.__cmd:
            doc = ""
            if type(self.__cmd[i]) is not str:
                if self.__cmd[i]["doc"] is not None:
                    doc += self.__cmd[i]["doc"]
                if len(self.__cmd[i]["args"]) != 0:
                    text += "Alias    "+ ", ".join(self.__cmd[i]["alias"])+" -> "+i+" "+" ".join(map(str, self.__cmd[i]["args"]))+" "+doc+"\n"
                else:
                    text += "Alias    "+ ", ".join(self.__cmd[i]["alias"])+" -> "+i+" "+doc+"\n"
        echo(text[:-1], anim=self.anim, cool=self.cool, color=self.color)

    def change_directory(self, path : str = home) -> None:
        "Allows you to change the location of the terminal in your files."
        if os.path.isdir(os.path.normpath(self.path+"\\"+path)):
            path = os.path.normpath(self.path+"\\"+path)
        else:
            path = os.path.normpath(path)
        if os.path.isdir(path):
            self.path = str(path).title()
        else:
            echo("The path is invalid.", anim=self.anim, cool=self.cool, color=self.color)

    def __decode(self, tpe: object, value: any) -> object:
        if tpe == inspect._empty:
            tpe = str
        try:
            for member in tpe.__args__:
                try:
                    return member(value)
                except ValueError: 
                    pass
        except AttributeError:
            return tpe(value)

    def run(self) -> None:
        "This method of the CLI object allows you to launch the CLI after you have created all your commands."
        if self.logs:
            write_logs(self.__cmd)
        while True:
            try:
                entry = shlex.split(prompt(self.prompt.format(self.user, self.path), anim=self.anim, cool=self.cool,  color=self.color, logs=self.logs).lower())
                cmd = self.__cmd[entry[0]]
                if isinstance(cmd, str):
                    cmd = self.__cmd[cmd]
                args = []
                for nmb, arg in enumerate(entry[1:len(cmd["args"])+1]):
                    args.append(self.__decode(cmd["types"][nmb], arg))
                cmd["function"](*args)
            except KeyboardInterrupt:
                break
            except KeyError:
                echo(self.not_exist.format(entry[0]), anim=self.anim, cool=self.cool, logs=self.logs, color=self.color)
            except Exception as e:
                echo(self.unexpected.format(e), anim=self.anim, cool=self.cool, logs=self.logs, color=self.color)

def echo(*values: object,
         sep: str = " ",
         end: str = "\n",
         anim: bool = True,
         cool: float | int = 0.1,
         color: tuple | str | None = None,
         logs: bool = False
         ) -> None:
    """
    The echo method works like the print method which is already implemented in python but has a progressive 
    display system if the value of the anim parameter is set to True and also has a logging system that 
    writes the text you enter to the daily logs which is by default enabled. The cool parameter corresponds
    to the exposure time before displaying the next character (in MS) of the text you have entered if the 
    anim parameter is set to True.

    Example of use::

        >>> import PyCLI
        >>> PyCLI.echo("Hello World", anim=True, cool=15, logs=True, end="\n", sep=" ")
    """
    output = sep.join(map(str, values))
    times =  cool / len(output)
    if anim:
        for char in output:
            print(colored(char, color), end="", flush=True)
            time.sleep(times)
        print(end=end)
    else:
        print(colored(output, color), end=end)

    if logs:
        write_logs(output)


def prompt(__prompt: object = "",
           anim: bool = True,
           cool: float | int = 0.1,
           color: tuple | str | None = None,
           logs: bool = False
           ) -> str:
    """
    The prompt method works like the input method which is already implemented in python but has a progressive display 
    system if the value of the anim parameter is set to True and also includes a logging system that writes the 
    text that the user will respond to in the daily logs. The logging system is enabled by default. The cool 
    parameter corresponds to the exposure time before displaying the next character (in MS) of the text you have entered
    if the anim parameter is set to True.

    Example of use::

        >>> import PyCLI
        >>> PyCLI.prompt("What's your name ?", anim=True, cool=15, logs=True, end="\n", sep=" ")
    """
    times =  cool / len(__prompt)
    if anim:
        for i in str(__prompt):
            print(colored(i, color), end="", flush=True)
            time.sleep(times)
    else:
        print(colored(str(__prompt), color), end="")
    returned = input()
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

    Example of use::

        >>> import PyCLI
        >>> PyCLI.write_logs("CLI was starting.")
    """
    text = sep.join(map(str, values)) + end
    if not os.path.exists("latest"):
        os.mkdir("latest")
    with open(f"latest/{datetime.today().date()}.log", "a", encoding="UTF-8") as file:
        file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")


def colored(text: str, 
            color: tuple | str | None = None
            ) -> str:
    """
    This method allows you to convert non-colored text to colored text. The color argument supports 
    tuples for writing the color code in rgb format and str for hexadecimal format.

    Examples of use::

        >>> import PyCLI
        >>> print(PyCLI.colored("Hello World", "FF0000"))

        >>> import PyCLI
        >>> print(PyCLI.colored("Hello World", (255, 0, 0)))
    """
    if isinstance(color, str):
        return f"\033[38;2;{int(color[0:2], 16)};{int(color[2:4], 16)};{int(color[4:6], 16)}m{text}\033[0m"
    elif isinstance(color, tuple):
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m"
    elif color is None:
        return text

def gram(debug=False) -> None:
    "Displays the amount of memory used overall by the program, the debug arguments allow you to display the amount of memory used by each variable."
    memory = 0
    all_vars = globals()
    for index in all_vars:
        imemory = sys.getsizeof(all_vars[index])
        if debug:
            print(index, imemory)
        memory += imemory
    print(f"[memory] {memory} bytes")