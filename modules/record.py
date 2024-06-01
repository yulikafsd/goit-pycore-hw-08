from fields import Name, Phone, Birthday
from errors import ValidationError


# Record: Клас для зберігання інформації про контакт. Кожен запис містить набір полів, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name):
# - зберігання об'єкта Name в окремому атрибуті
        self.name = Name(name)
# - зберігання списку об'єктів Phone в окремому атрибуті
        self.phones = []
#  поле birthday для дня народження
        self.birthday = None


# - Додавання телефонів add_phone
    def add_phone(self, phone):     # додати перевірку, чи додано вже такий номер
        try:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
            return f"{self.name.value}'s record was updated with a new number: {phone}"
        except ValidationError as e:
            return f"ERROR! No phone number was addded! {e}"


# Повідомлення, що  у контакта немає вказаного номера, вивід наявних номерів
    def wrong_phone_alert(self, phone):
        return f'User {self.name} has no phone {phone}.\nPlease, choose one of the existing phone numbers:\n{chr(10).join(p.value for p in self.phones)}'


# - Пошук телефону (об'єкту Phone) - find_phone
    def find_phone(self, searched_phone):
        try:
            found_phone = list(filter(lambda phone: phone.value == searched_phone, self.phones))[0]
            return found_phone
        except IndexError:
            return self.wrong_phone_alert(searched_phone)


# - Редагування телефонів edit_phone
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                try:
                    new_phone_obj = Phone(new_phone)
                    self.phones.append(new_phone_obj)
                except ValidationError as e:
                    return f"ERROR! No phone number was addded! {e}"
                else:
                    self.phones.remove(phone)
                    return f"{self.name.value}'s record was updated with a new number: {new_phone}"
        return self.wrong_phone_alert(old_phone)


# - Видалення телефонів remove_phone
    def remove_phone(self, old_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.remove(phone)
                return
        return self.wrong_phone_alert(old_phone)


# - Додавання дня народження до контакту
    def add_birthday(self, birthday):
        # Якщо у користувача ще немає дня народження, записати новий
        if self.birthday is None:
            try:
                self.birthday = Birthday(birthday)
                return f"Birthday {birthday} is added to {self.name}'s record"
            except ValidationError as e:
                return f"ERROR! {e}"
            except ValueError as e:
                return f"ERROR! Please, choose a real date, {e}"
        
        # якщо вже є день народження, спитати, чи перезаписати
        else:
            print(f"Contact {self.name.value} already has a birthday record")
            user_input = input(f"Would you like to change {self.name.value}'s birth date? Y/N: ")
            if user_input.lower() == 'n':
                return "Nothing changed"
            else:
                try:
                    self.birthday = Birthday(birthday)
                    return f"Birth date of {self.name} was changed to {birthday}"
                except ValidationError as e:
                    return f"ERROR! {e}"


    def __str__(self):
        return f"Contact name: {self.name.value}; phones: {', '.join(p.value for p in self.phones)}; birthday: {self.birthday.value if self.birthday is not None else self.birthday}"