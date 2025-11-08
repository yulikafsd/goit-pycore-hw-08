from collections import UserDict
from record import Record
from datetime import datetime, timedelta


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"New record for {record.name.value} was added to the book:\n{self.data}"

    def find(self, name):
        record = self.data.get(name)
        return record if record is not None else None

    def delete(self, name):
        record = self.find(name)
        if record:
            del self.data[name]
            return f"{name} deleted from contacts"
        else:
            return f"No contact {name} was found"

    def get_upcoming_birthdays(self) -> list:
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday and record.birthday.value:
                birthday = record.birthday.value.date()
                year = (
                    today.year
                    if birthday.replace(year=today.year) >= today
                    else today.year + 1
                )
                congratulation_date = birthday.replace(year=year)

                if 0 <= (congratulation_date - today).days <= 7:
                    # Якщо день народження випадає на вихідні — переносимо на понеділок
                    if congratulation_date.weekday() == 5:
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:
                        congratulation_date += timedelta(days=1)

                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": congratulation_date.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )

        return upcoming_birthdays
