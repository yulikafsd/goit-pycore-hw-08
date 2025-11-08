from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(value=name)


class Phone(Field):
    def __init__(self, number):
        super().__init__(value=self.validate_number(number))

    def validate_number(self, number):
        number = number.strip()
        if len(number) == 10 and number.isdigit():
            return number
        else:
            raise ValueError("Wrong number length, need 10 digits")

    def update(self, new_number):
        validated = self.validate_number(new_number)
        self.value = validated


class Birthday(Field):
    def __init__(self, value):

        if not isinstance(value, str):
            raise ValueError("Birthday must be a string in format DD.MM.YYYY")

        if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date value. Use DD.MM.YYYY")

        super().__init__(value=date_obj)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # поле не обов'язкове, але може бути тільки одне

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.update(new_phone)
                return True
        return False

    def find_phone(self, number):
        found_phone = None
        for phone_obj in self.phones:
            if phone_obj.value == number:
                found_phone = phone_obj
                break
        if found_phone:
            return found_phone

    def remove_phone(self, number):
        for phone_obj in self.phones:
            if phone_obj.value == number:
                self.phones.remove(phone_obj)
                break

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __str__(self):
        bday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{bday_str}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"Record for {record.name.value} was added to the book:\n{self.data}"

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self) -> list:
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not (record.birthday and record.birthday.value):
                continue

            birthday = record.birthday.value.date()
            year = (
                today.year
                if birthday.replace(year=today.year) >= today
                else today.year + 1
            )
            congratulation_date = birthday.replace(year=year)

            if 0 <= (congratulation_date - today).days <= 7:
                # Якщо день народження випадає на вихідні — переносимо на понеділок
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming_birthdays


MESSAGES = {
    ValueError: "Wrong number of arguments",
    IndexError: "Please enter a name after the command. Usage: phone <name>",
    TypeError: "Invalid command format or wrong number of arguments",
}


# Decorator for exceptions
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_text = str(e)
            if any(
                phrase in err_text
                for phrase in [
                    "Wrong number length",
                    "Invalid date format",
                    "Invalid date value",
                ]
            ):
                return err_text
            for e_type, msg in MESSAGES.items():
                if isinstance(e, e_type):
                    return msg
            return f"Unexpected error: {e}"

    return inner


def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    updated = record.edit_phone(old_phone, new_phone)
    if updated:
        return f"Phone for {name} updated from {old_phone} to {new_phone}."
    else:
        return f"Phone {old_phone} not found for {name}."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found"
    phones = "; ".join(p.value for p in record.phones)
    return f"{name}'s phones: {phones}" if phones else f"{name} has no phone numbers."


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved yet."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, new_birthday, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    if record.birthday:
        message = f"Birthday for {name} updated to {new_birthday}"
    else:
        message = f"Birthday for {name} added: {new_birthday}"
    record.add_birthday(new_birthday)
    return message


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    if not record.birthday:
        return f"Contact {name} has no birthday yet"
    return f"{name}'s birthday: {record.birthday}"


@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{d['name']}: {d['congratulation_date']}" for d in upcoming)


def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
