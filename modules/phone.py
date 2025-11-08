from field import Field


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
