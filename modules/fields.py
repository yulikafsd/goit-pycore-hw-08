from errors import ValidationError
from datetime import datetime
import re


# Field: Базовий клас для полів запису.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)


# Name: Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    # реалізація класу - обов'язкове поле
	def __init__(self, name):
         super().__init__(name)


# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, phone):
        # перевірка коректності даних
        if len(phone) == 10 and phone.isdigit():
            super().__init__(phone)
        else:
            raise ValidationError("Phone must contain 10 digits and consist of digits only")


# КЛас для зберігання дати народження. Має валідацію формату (ДД.ММ.ГГГГ)
class Birthday(Field):
    def __init__(self, birthday):
        # перевірка коректності даних
            if re.match(r'(\d{2}\.\d{2}\.\d{4})', birthday):
                # перетворення рядку на об'єкт datetime
                super().__init__(datetime.strptime(birthday, '%d.%m.%Y').date())
            else:
                raise ValidationError(f'Invalid date format of {birthday}. Use DD.MM.YYYY')