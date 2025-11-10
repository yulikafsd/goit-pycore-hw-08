from enum import Enum
from modules import (
    load_data,
    save_data,
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)


class Command_Use(Enum):
    ADD = "add [name] [phone]"
    CHANGE = "change [name] [old_phone] [new_phone]"
    PHONE = "phone [name]"
    ALL = "all"
    ADD_BIRTHDAY = "add-birthday [name] [birthday]"
    SHOW_BIRTHDAY = "show-birthday [name]"
    BIRTHDAYS = "birthdays"
    HELLO = "hello"
    CLOSE = "close"
    EXIT = "exit"


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
                print("Invalid command. The following commands are available:")
                for cmd in Command_Use:
                    print(f" - {cmd.value}")


if __name__ == "__main__":
    main()
