from .utils import input_error
from .addressbook import AddressBook
from .record import Record


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        record = Record(name_capitalized)
        book.add_record(record)

    else:
        user_input = input(
            f"Contact {name_capitalized} already exists.\nAdd another phone number to the contact? Y/N: "
        )
        if user_input.lower() == "n":
            return "Nothing changed"
    return record.add_phone(phone)


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        user_input = input(
            f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: "
        )
        if user_input.lower() == "y":
            return add_contact([name_capitalized, new_phone], book)
        else:
            return "Nothing changed"
    return record.edit_phone(old_phone, new_phone)


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return f"Contact with name {name_capitalized} was not found"
    return (
        f"{name_capitalized}'s phones: {', '.join([p.value for p in record.phones])}"
        if record.phones
        else f"{name_capitalized} has no phone numbers yet."
    )


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts were found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, new_birthday, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return "Contact with name {name_capitalized} was not found."
    return record.add_birthday(new_birthday)


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return "Contact with name {name_capitalized} was not found."
    if not record.birthday:
        return f"Contact {name_capitalized} has no birthday yet"
    return f"{name_capitalized}'s birthday: {record.birthday}"


@input_error
def birthdays(book: AddressBook):
    if not book.data:
        return "No contacts were found."
    upcoming_bds = book.get_upcoming_birthdays()
    if not upcoming_bds:
        return "No birthdays in the next 7 days."
    return ", ".join(
        f"{user['name']}: {user['congratulation_date']}" for user in upcoming_bds
    )
