from .errors import ValidationError
from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, number):
        super().__init__(self.validate_number(number))

    def validate_number(self, number):
        number = number.strip()
        if len(number) == 10 and number.isdigit():
            return number
        else:
            raise ValidationError(
                "Phone must contain 10 digits and consist of digits only"
            )

    def update(self, new_number):
        validated = self.validate_number(new_number)
        self.value = validated


class Birthday(Field):
    def __init__(self, birthday):

        if isinstance(birthday, str) and re.match(r"\d{2}\.\d{2}\.\d{4}$", birthday):
            super().__init__(datetime.strptime(birthday, "%d.%m.%Y"))

        else:
            raise ValidationError(f"Invalid date format of {birthday}. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
