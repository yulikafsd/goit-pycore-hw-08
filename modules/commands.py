from input_error import *
from address_book import AddressBook
from record import Record


# Parse command line 
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    name_norm = name.capitalize()
    record = book.find(name_norm)

    # Додати якщо ще немає
    if record is None:
        record = Record(name_norm)
        book.add_record(record)
    
    # Чи додати номер, якщо контакт вже є
    else:
        user_input = input(f"Contact {name_norm} already exists.\nAdd another phone number to the contact? Y/N: ")
        if user_input.lower() == 'n':
            return "Nothing changed"
    
    # Додати номер телефону до нового, або до існуючого контакту 
    return record.add_phone(phone)


# Змінити телефонний номер для вказаного контакту
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    name_norm = name.capitalize()
    record = book.find(name_norm)
    
    # Якщо ім'я не знайдено, пропонуємо додати
    if record is None:
        user_input = input("Contact with this name was not found.\nAdd a new contact? Y/N: ")
        if user_input.lower() == 'y':
            return add_contact([name, new_phone], book)
        else:
            return "Nothing changed"

    # Якщо ім'я знайдено, змінюємо
    else:
        return record.edit_phone(old_phone, new_phone)


# Показати телефонний номер для вказаного контакту
@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    name_norm = name.capitalize()
    record = book.find(name_norm)

    # Повідомлення про помилку, якщо ім'я не знайдено
    if record is None:
        return f"Contact with name {name_norm} was not found"
    
    # Якщо знайдено і в контакта є телефони, вивід: [номер_телефону, ]
    else:
        if len(record.phones) > 0: 
            return f"{name_norm}'s phones: {record.phones}"
        
        # Якщо телефонів немає:
        else:
            return f"{name_norm} has no phones yet"


# Показати всі контакти в адресній книзі
@input_error
def show_all(book: AddressBook):
    
    # Якщо контактів немає:
    if len(book) == 0:
        return "No contacts were found"
    
    # Якщо контакти є:
    contacts_string = ""
    for record in book.values():
        contacts_string += f"\n{record}" 
    return f"Your contacts: {contacts_string}"


# Додати дату народження для вказаного контакту
@input_error
def add_birthday(args, book: AddressBook):
    name, bd, *_ = args
    name_norm = name.capitalize()
    record = book.find(name_norm)

    # Якщо контакту немає:
    if record is None:
        return f"Contact with name {name_norm} was not found"
    
    # Якщо є, додаємо день народження
    else:
        return record.add_birthday(bd)


# Показати дату народження для вказаного контакту
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    name_norm = name.capitalize()
    record = book.find(name_norm)
    
    # Якщо контакту немає:
    if record is None:
        return f"Contact with name {name_norm} was not found"
    
    # Якщо знайдено, перевірка, чи записаний день народження
    else:
        if record.birthday is None: 
            return f"{name_norm} has no birthday yet"
        else:
            return f"{name_norm}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


# Показати дні народження, які відбудуться протягом наступного тижня
@input_error
def birthdays(book: AddressBook):
    if len(book) == 0:
        return "No contacts were found"
    else:
        return f"Your contacts: {book.get_upcoming_birthdays()}"