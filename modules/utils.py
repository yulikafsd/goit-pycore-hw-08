def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            match func.__name__:
                case "add_contact":
                    return "Wrong format. Usage: add [contact_name] [phone_number]"
                case "change_contact":
                    return "Wrong format. Usage: change [contact_name] [old_phone_number] [new_phone_number]"
                case "add_birthday":
                    return "Wrong format. Usage: add-birthday [contact_name] [birthday]"
                case "show_birthday":
                    return "Wrong format. Usage: show-birthday [contact_name]"
                case _:
                    return "ValueError"
        except KeyError:
            return "KeyError"
        except IndexError:
            if func.__name__ == "show_phone":
                return "Wrong format. Usage: phone [contact_name]."
            else:
                return "IndexError"

    return inner
