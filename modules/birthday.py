from field import Field


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
