import os
import subprocess
import sys


BUILTIN_COMMANDS = {
    "echo": lambda args: sys.stdout.write(' '.join(args) + '\n'),
    "type": lambda args: type_function(args),
    "pwd": lambda args: sys.stdout.write(os.getcwd() + '\n'),
    "cd": lambda args: change_directory(args[0] if args else ""),
    "exit": lambda args: sys.exit(0),
}

def change_directory(path):
    try:
        if path == "~":
            os.chdir(os.path.expanduser("~"))
        elif path != "":
            os.chdir(path)

    except FileNotFoundError:
        sys.stderr.write(f"cd: {path}: No such file or directory\n")

def find_executable(command):
    if 'PATH' not in os.environ:
        return None
    for path in os.environ['PATH'].split(os.pathsep):
        full_path = os.path.join(path, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def type_function(args):
    if not args:
        return
    command = args[0]
    if command in BUILTIN_COMMANDS:
        sys.stdout.write(f"{command} is a shell builtin\n")
    elif path := find_executable(command):
        sys.stdout.write(f"{command} is {path}\n")
    else:
        sys.stdout.write(f"{command}: not found\n")

def parse_input(user_input):
    """Parse raw input, preserving spaces inside quotes"""
    args = []
    current = ""
    in_quote = False
    quote_char = None
    skip_next = False

    for i in range(len(user_input)):
        char = user_input[i]
        if skip_next:
            skip_next = False
            continue
        if char == '\\' and i + 1 < len(user_input) and in_quote:
            current += user_input[i+1]
            skip_next = True
        elif char in ("'", '"') and not in_quote:
            in_quote = True
            quote_char = char
        elif char == quote_char:
            in_quote = False
            quote_char = None
        elif char == ' ' and not in_quote:
            if current:
                args.append(current)
                current = ""
        else:
            current += char

    if current:
        args.append(current)

    return args


def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        if not user_input:
            continue
        parts = parse_input(user_input)
        if not parts:
            continue
        command, *args = parts

        if command in BUILTIN_COMMANDS:
            BUILTIN_COMMANDS[command](args)
        elif find_executable(command):
            subprocess.run([command] + args)
        else:
            sys.stdout.write('{}: command not found\n'.format(command))

if __name__ == "__main__":
    main()