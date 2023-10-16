# HotFuzz Control Panel

HotFuzz Control Panel is a shell script calling utility based on [HotFuzz](https://github.com/megahomyak/hotfuzz).

## Installation

* `pip install hotfuzz_control_panel`

## Configuration

Use your system's configurations directory, there create a directory called `hotfuzz_control_panel`, and there create a file called `commands` (simply `commands`, no extension). If you're still unsure as to where to put the file, just run `python -m hotfuzz_control_panel` and look at the error message.

The `commands` file should look like that:

```
Command Name
>first line of script
>second line of script
>third line of script
>...

Another Command Name
>first line
>second line
>...

Yet Another Command
>something
```

...you get the idea.

## Running

* Execute `python -m hotfuzz_control_panel`

If you see a `UnexpectedIndentation` exception, it means that there is a line somewhere at the beginning of your `commands` file that is indented (with `>`) without any command names preceding it.

If you see a `HotCollision` exception, it means that at least one command from the ones you've provided has a sequence of big letters that starts with the full sequence of some other command. This will make the command with the longer sequence uncallable in the "Hot" mode, and thus it's prohibited.
