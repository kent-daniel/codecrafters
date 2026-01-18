import os
import subprocess
import sys

BUILTIN_COMMANDS = {
    "echo": lambda args: sys.stdout.write(' '.join(args) + '\n'),
    "type": lambda args: type_function(args),
    "pwd": lambda args: sys.stdout.write(os.getcwd() + '\n'),
    "exit": lambda args: sys.exit(0),
}


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

def main():
    while True:
        sys.stdout.write("$ ")
        parts = input().split()
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
