import os
from hotfuzz import HotFuzz
from appdirs import user_config_dir
from pathlib import Path
import re
import subprocess

config_path = Path(user_config_dir(appname="hotfuzz_control_panel")) / "commands"

with open(config_path, encoding="utf-8") as f:
    config = f.read()

class UnexpectedIndentation(Exception):
    pass

commands_list = {}
last_group = None
for line in config.splitlines():
    if line.strip() == "":
        continue
    if re.match(r"\s", line):
        if last_group is None:
            raise UnexpectedIndentation()
        commands_list[last_group].append(line.lstrip())
    else:
        last_group = line
        commands_list[line] = []

names = list(commands_list.keys())
hotfuzz = HotFuzz(names, initially_invisible=False)
result = hotfuzz.run()
if result is not None:
    commands_list = commands_list[names[result]]
    process = subprocess.Popen(
        os.linesep.join(commands_list),
        shell=True,
        close_fds=False,
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
