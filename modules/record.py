from .fields import Name, Phone, Birthday
from .errors import ValidationError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # поле не обов'язкове, але може бути тільки одне

    def add_phone(self, number):
        for phone_obj in self.phones:
            if phone_obj.value == number:
                return f"{self.name.value}'s record already has the number: {number}"
        try:
            self.phones.append(Phone(number))
            return f"{self.name.value}'s record was updated with a new number: {number}"
        except ValidationError as e:
            return f"ERROR! No phone number was addded! {e}"

    def wrong_phone_alert(self, phone):
        return f"User {self.name} has no phone {phone}.\nPlease, choose one of the existing phone numbers:\n{chr(10).join(p.value for p in self.phones)}"

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                try:
                    phone_obj.update(new_phone)
                    return f"{self.name.value}'s record was updated with a new number: {new_phone}"
                except ValidationError as e:
                    return f"ERROR! No phone number was addded! {e}"
        return self.wrong_phone_alert(old_phone)

    def find_phone(self, searched_phone):
        try:
            found_phone = list(
                filter(lambda phone: phone.value == searched_phone, self.phones)
            )[0]
            return found_phone
        except IndexError:
            return self.wrong_phone_alert(searched_phone)

    def remove_phone(self, number):
        for phone_obj in self.phones:
            if phone_obj.value == number:
                self.phones.remove(phone_obj)
                return f"User {self.name}'s phone {number} was removed.\nThe remaining phone numbers are:\n{chr(10).join(p.value for p in self.phones)}"
        return self.wrong_phone_alert(number)

    def add_birthday(self, birthday):
        if self.birthday is None:
            try:
                self.birthday = Birthday(birthday)
                return f"Birthday {birthday} is added to {self.name}'s record"
            except ValidationError as e:
                return f"ERROR! {e}"
            except ValueError as e:
                return f"ERROR! Please, choose a real date, {e}"

        else:
            print(f"Contact {self.name.value} already has a birthday record")
            user_input = input(
                f"Would you like to change {self.name.value}'s birth date? Y/N: "
            )
            if user_input.lower() == "n":
                return "Nothing changed"
            else:
                try:
                    self.birthday = Birthday(birthday)
                    return f"Birth date of {self.name} was changed to {birthday}"
                except ValidationError as e:
                    return f"ERROR! {e}"

    def __str__(self):
        bday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{bday_str}"
