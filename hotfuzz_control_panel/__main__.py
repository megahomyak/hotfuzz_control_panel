import os
from hotfuzz import HotFuzz
from appdirs import user_config_dir
from pathlib import Path
import re

config_path = Path(user_config_dir(appname="hotfuzz")) / "commands"

with open(config_path, encoding="utf-8") as f:
    config = f.read()

class UnexpectedIndentation(Exception):
    pass

class ReturnCodeOfCommandIsNotNull(Exception):
    pass

commands = {}
last_group = None
for line in config.splitlines():
    if line.strip() == "":
        continue
    if re.match(r"\s", line):
        if last_group is None:
            raise UnexpectedIndentation()
        commands[last_group].append(line.lstrip())
    else:
        last_group = line
        commands[line] = []

names = list(commands.keys())
hotfuzz = HotFuzz(names, initially_invisible=False)
result = hotfuzz.run()
if result is not None:
    commands_list = commands[names[result]]
    for command in commands_list:
        print(command)
        if os.system(command) != 0:
            raise ReturnCodeOfCommandIsNotNull()