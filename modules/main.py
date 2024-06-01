from address_book import AddressBook
from commands import *


def main():
    contacts = AddressBook()

    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args,contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case 'add-birthday':
                print(add_birthday(args, contacts))
            case 'show-birthday':
                print(show_birthday(args, contacts))
            case 'birthdays':
                print(birthdays(contacts))
            case _:
                    print('''Invalid command. The following commands are available:\n'''
                        '''add, change, phone, all, add-birthday, show-birthday, birthdays''')

if __name__ == "__main__":
    main()