from .record import Record
from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"New record for {record.name.value} was added to the book:\n{self.data}"

    def find(self, name):
        record = self.data.get(name)
        return record if record else None

    def delete(self, name):
        record = self.data.get(name)
        if not record:
            return f"No contact {name} was found"
        del self.data[name]
        return f"{name} deleted from contacts"

    def get_upcoming_birthdays(self) -> list:
        current_date = datetime.today().date()

        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                contact_bd = record.birthday.value.date()
                current_year = current_date.year
                is_coming = contact_bd.replace(year=current_year) >= current_date
                congratulation_year = (
                    current_year if is_coming else current_date.year + 1
                )
                congratulation_date = contact_bd.replace(year=congratulation_year)
                is_next_week = 0 < (congratulation_date - current_date).days <= 7

                if is_next_week:

                    bd_weekday = congratulation_date.weekday()
                    if bd_weekday == 5:
                        congratulation_date += timedelta(days=2)
                    if bd_weekday == 6:
                        congratulation_date += timedelta(days=1)

                    congrat_date_string = congratulation_date.strftime("%d.%m.%Y")
                    coming_bd = {
                        "name": record.name.value,
                        "congratulation_date": congrat_date_string,
                    }
                    upcoming_birthdays.append(coming_bd)

        return upcoming_birthdays
