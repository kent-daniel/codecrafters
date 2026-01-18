import sys

BUILTIN_COMMANDS = {
    "echo": lambda args: sys.stdout.write(' '.join(args) + '\n'),
    "type": lambda args: sys.stdout.write(f'{args[0]} is a shell builtin\n') if args and args[0] in BUILTIN_COMMANDS else sys.stdout.write(f'{args[0]}: not found\n'),
    "exit": lambda args: sys.exit(0),
}

def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command, *args = input().split()

        if command in BUILTIN_COMMANDS.keys():
            BUILTIN_COMMANDS[command](args)
        else:
            sys.stdout.write('{}: command not found\n'.format(command))

if __name__ == "__main__":
    main()
