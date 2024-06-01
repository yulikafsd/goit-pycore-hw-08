# Декоратор для обробки невірного введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            match func.__name__:
                case 'add_contact':
                    return "Wrong format. Please, enter: add [contact_name] [phone_number]"
                case 'change_contact':
                    return "Wrong format. Please, enter: change [contact_name] [old_phone_number] [new_phone_number]"
                case 'add_birthday':
                    return "Wrong format. Please, enter: add-birthday [contact_name] [birthday]"
                case 'show_birthday':
                    return "Wrong format. Please, enter: show-birthday [contact_name]"
                case _:
                    return "ValueError"
        except KeyError:
            return "KeyError"
        except IndexError:
            if func.__name__ == 'show_phone':
                return "Wrong format. Please, enter: phone [contact_name]."
            else:
                return "IndexError"
    return inner
