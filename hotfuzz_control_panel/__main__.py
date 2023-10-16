import os
from hotfuzz import HotFuzz
from appdirs import user_config_dir
from pathlib import Path

config_path = Path(user_config_dir(appname="hotfuzz_control_panel", appauthor=False)) / "commands"

with open(config_path, encoding="utf-8") as f:
    config = f.read()

class UnexpectedIndentation(Exception):
    pass

commands = {}
last_group = None
for line in config.splitlines():
    if line.lstrip() == "":
        continue
    if line.startswith(">"):
        # This is a line from a group
        line = line[1:] # Trimming the ">"
        try:
            commands[last_group].append(line)
        except KeyError:
            raise UnexpectedIndentation()
    else:
        # This is a group name
        last_group = line
        commands[line] = []

names = list(commands.keys())
hotfuzz = HotFuzz(names, initially_invisible=False)
result = hotfuzz.run()
if result is not None:
    commands_list = commands[names[result]]
    commands_string = os.linesep.join(commands_list)
    os.system(commands_string)
