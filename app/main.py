import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        
        match command:
            case "exit":
                break
            case _:
                sys.stdout.write('{}: command not found\n'.format(command))


if __name__ == "__main__":
    main()
