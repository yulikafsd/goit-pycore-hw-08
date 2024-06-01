from datetime import date
from collections import UserDict


# AddressBook: Клас для зберігання та управління записами
class AddressBook(UserDict):


# - Додавання записів - add_record, який додає запис до self.data.
    def add_record(self, record):
        self.data[record.name.value] = record
        print(f"New record for {record.name.value} was added")


# - Пошук записів за іменем - find, який знаходить запис за ім'ям
    def find(self, name):
        record = self.data.get(name)
        return record if record is not None else None


# - Видалення записів за іменем - delete, який видаляє запис за ім'ям
    def delete(self, name):
        record = self.find(name)
        if record:
            del self.data[name]
            return f"{name} deleted from contacts"
        else:
            return f"No contact {name} was found"


# - Пошук найближчих днів народжень
    def get_upcoming_birthdays(self):
        upcoming_bd_users = []
        current_date = date.today()

        for user in self.data:
            user_birthday = self.data[user].birthday
            
            if user_birthday:
                this_year_bd = date(current_date.year, user_birthday.value.month, user_birthday.value.day)
                is_coming = current_date < this_year_bd
                is_next_week = (this_year_bd - current_date).days < 7
                
                # визначення днів народження на 7 днів вперед:
                if is_coming and is_next_week:
                    
                    # Обробка випадків, коли дні народження припадають на вихідні:
                    bd_weekday = this_year_bd.weekday()
                    
                    match bd_weekday:
                        case 5:
                            congrat_date = date(current_date.year, user_birthday.month, (user_birthday.day + 2))
                        case 6:
                            congrat_date = date(current_date.year, user_birthday.month, (user_birthday.day + 1))
                        case _:
                            congrat_date = this_year_bd
                    
                    congrat_date_string = congrat_date.strftime('%d.%m.%Y')
                    bd_user = {'name' : user, 'congratulation_date': congrat_date_string}
                    upcoming_bd_users.append(bd_user)
            
        return f"List of congratultaions this week:{upcoming_bd_users}"
