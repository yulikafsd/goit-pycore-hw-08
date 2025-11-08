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
