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
import platform
import colorama

GUI = f"""{colorama.Fore.YELLOW}                .                       
{colorama.Fore.YELLOW}             .~5P.                      
{colorama.Fore.YELLOW}           :JB&&G:                      
{colorama.Fore.YELLOW}         ^YB&&&#P^                      
{colorama.Fore.YELLOW}       :JGB####B5!                      
{colorama.Fore.YELLOW}     .~5GBBGGGGG5J:                     
{colorama.Fore.YELLOW}    .~5PPPPPP5555J?:                    
{colorama.Fore.YELLOW}    .J555YYYYJJJJJ??!:                  8888888 8888888b. {colorama.Fore.LIGHTRED_EX}      88888888888                888          
{colorama.Fore.YELLOW}    .!5YYJJ???77777!!7!^.                 888   888   Y88b{colorama.Fore.LIGHTRED_EX}          888                    888         
{colorama.Fore.LIGHTRED_EX}   !7:~{colorama.Fore.YELLOW}JJJ??777!!!~~~~~!!^.               888   888    888{colorama.Fore.LIGHTRED_EX}          888                    888         
{colorama.Fore.LIGHTRED_EX}  ^PP57{colorama.Fore.YELLOW}^~7?77!!!~~~^^^~~~!!^              888   888   d88P{colorama.Fore.LIGHTRED_EX}          888   .d88b.   .d88b.  888 .d8888b 
{colorama.Fore.LIGHTRED_EX} .Y5555Y!:{colorama.Fore.YELLOW}^!77!~~~^^^^^^~~!!!.            888   8888888P" {colorama.Fore.LIGHTRED_EX}          888  d88""88b d88""88b 888 88K     
{colorama.Fore.LIGHTRED_EX} !5YJJJJJ?~.{colorama.Fore.YELLOW}.^!!~~^^^^~~~~!!7?:           888   888       {colorama.Fore.LIGHTRED_EX}          888  888  888 888  888 888 "Y8888b.
{colorama.Fore.LIGHTRED_EX}.JJ???777777: {colorama.Fore.YELLOW}.^!!~~~~~~!!!77?7           888   888       {colorama.Fore.LIGHTRED_EX}          888  Y88..88P Y88..88P 888      X88
{colorama.Fore.LIGHTRED_EX}:J?77!!!~~~!!~. {colorama.Fore.YELLOW}.~7!!!!!7777?J7         8888888 888       {colorama.Fore.LIGHTRED_EX}          888   "Y88P"   "Y88P"  888  88888P'  
{colorama.Fore.LIGHTRED_EX}.??7!!~~^^^^~!!. {colorama.Fore.YELLOW}.~?77777???J?.         
{colorama.Fore.LIGHTRED_EX} ^?77!~~^^^~~!7^ {colorama.Fore.YELLOW}.^?????JJJJ!.          
{colorama.Fore.LIGHTRED_EX}  .~777!!!!!!!7! {colorama.Fore.YELLOW}.~JJJJYYJ!.            
{colorama.Fore.LIGHTRED_EX}    .:!7?7777??~ {colorama.Fore.YELLOW}.!YY5YJ~.              
{colorama.Fore.LIGHTRED_EX}       .^!?JJJY^ {colorama.Fore.YELLOW}.J5J!:                 
{colorama.Fore.LIGHTRED_EX}          .:!JY. {colorama.Fore.YELLOW}.~.                   """
print(GUI)

class CLI(Exception):
    def __init__(self,
                 prompt: str = "Python@CLI\\>",
                 not_exist: str = "This command does not exist.\nDo help to get the list of existing commands.",
                 logs: bool = True,
                 animation: bool = True,
                 cooldown: float | int = 0.1,
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
            >>> cli = PyCLI.CLI(prompt="Python@CLI\\>", logs=True, animation=True, cooldown=15, help_cmd=True, not_exist="This command does not exist.\nDo help to get the list of existing commands.")
            >>> @cli.command()
            >>> def hello_world():
            >>>     print("Hello World")
            >>> cli.run()
        """
        self.__cmd = []
        self.prompt = prompt
        self.not_exist = not_exist
        self.logs = logs
        self.animation = animation
        self.cooldown = cooldown

        match platform.system():
            case "Windows": self.__clear_cmd = "cls"
            case "Linux" | "Darwin": self.__clear_cmd = "clear"

        if help_cmd:
            @self.command(alias=["?"], doc=self.help.__doc__)
            def help() -> None:
                self.help()
        else: 
            del self.help

        @self.command(alias=["exit"], doc=self.leave.__doc__)
        def leave() -> None:
            self.leave()

        @self.command(alias=[self.__clear_cmd], name="clear-host", doc=self.clear_host.__doc__)
        def clear_host() -> None:
            self.clear_host()

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

        Exemples usages::

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

                exist = False
                for nmb, value in enumerate(self.__cmd):
                    for i in alias:
                        for j in value["alias"]:
                            if i == j:
                                raise CLI(f'[cmd: {value["name"]}] Alias "{i}" is already used.')
                    if value["name"] == name:
                        self.__cmd[nmb] = {
                            "name": name,
                            "doc": doc,
                            "function": func,
                            "args": args,
                            "types": types,
                            "alias": alias,
                        }
                        exist = True
                if not exist:
                    self.__cmd.append({
                        "name": name,
                        "doc": doc,
                        "function": func,
                        "args": args,
                        "types": types,
                        "alias": alias,
                    })
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
        print(GUI)

    def help(self) -> None:
        "Displays info about terminal commands."
        text = ""
        for i in self.__cmd:
            doc = ""
            if i["doc"] is not None:
                doc += i["doc"]
            text += "Alias    "+ ", ".join(i["alias"])+" -> "+i["name"]+" "+" ".join(map(str, i["args"]))+doc+"\n"
        echo(text[:-1], animation=self.animation, cooldown=self.cooldown, logs=False)

    def __decode(self, tpe: object, value: any) -> object:
        try:
            for member in tpe.__args__:
                print(member)
                try:
                    return member(value)
                except ValueError: 
                    pass
        except AttributeError:
            return tpe(value)

    def run(self) -> None:
        "This method of the CLI object allows you to launch the CLI after you have created all your commands."
        if self.logs: 
            write_logs(*self.__cmd)
        while True:
            try:
                self.__cmd = sorted(self.__cmd, key=lambda x: x["name"])
                entry = prompt(self.prompt, animation=self.animation, cooldown=self.cooldown).lower()
                exist = False
                for cmd in self.__cmd:
                    if cmd["name"] == entry.split(" ")[0] or entry.split(" ")[0] in cmd["alias"]:
                        exist = True
                        args = []
                        for nmb, arg in enumerate(entry.split(" ")[1:len(cmd["args"])+1]):
                            args.append(self.__decode(cmd["types"][nmb], arg))
                        cmd["function"](*args)
                        break
                if not exist: 
                    echo(self.not_exist, animation=self.animation, cooldown=self.cooldown, logs=self.logs)
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(e)
                continue

def echo(*values: object,
         sep: str = " ",
         end: str = "\n",
         animation: bool = True,
         cooldown: float | int = 0.1,
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
           cooldown: float | int = 0.1,
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
    with open(f"latest/{datetime.today().date()}.log", "a", encoding="UTF-8") as file:
        file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")