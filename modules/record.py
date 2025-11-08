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
