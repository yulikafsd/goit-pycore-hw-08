from modules.pickle_data import load_data, save_data
from modules.input_parser import parse_input
from modules.commands import *


def main():
    book = load_data()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if not command:
            continue

        match command:
            case "close" | "exit":
                print("Good bye!")
                save_data(book)
                break

            case "hello":
                print("How can I help you?")

            case "add":
                print(add_contact(args, book))

            case "change":
                print(change_contact(args, book))

            case "phone":
                print(show_phone(args, book))

            case "all":
                print(show_all(book))

            case "add-birthday":
                print(add_birthday(args, book))

            case "show-birthday":
                print(show_birthday(args, book))

            case "birthdays":
                print(birthdays(book))

            case _:
                print(
                    """Invalid command\n
                    The following commands are available:\n
                    add [name] [phone]\n
                    change [name] [old_phone] [new_phone]\n
                    phone [name]\n
                    all\n
                    add-birthday [name] [birthday]\n
                    show-birthday [name]\n
                    birthdays\n
                    hello\n
                    close\n
                    exit\n"""
                )


if __name__ == "__main__":
    main()
