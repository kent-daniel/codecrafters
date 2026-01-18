import os
import sys

BUILTIN_COMMANDS = {
    "echo": lambda args: sys.stdout.write(' '.join(args) + '\n'),
    "type": lambda args: type_function(args),
    "exit": lambda args: sys.exit(0),
}


def type_function(args):
    if not args:
        return
    command = args[0]
    if command in BUILTIN_COMMANDS:
        sys.stdout.write(f"{command} is a shell builtin\n")
        return
    elif 'PATH' in os.environ:
        paths = os.environ['PATH'].split(os.pathsep)
        for path in paths:
            full_path = os.path.join(path, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                sys.stdout.write(f"{command} is {full_path}\n")
                return
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
        else:
            sys.stdout.write('{}: command not found\n'.format(command))

if __name__ == "__main__":
    main()
