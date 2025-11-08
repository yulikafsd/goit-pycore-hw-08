MESSAGES = {
    ValueError: "Wrong number of arguments",
    IndexError: "Please enter a name after the command. Usage: phone <name>",
    TypeError: "Invalid command format or wrong number of arguments",
}


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_text = str(e)
            if any(
                phrase in err_text
                for phrase in [
                    "Wrong number length",
                    "Invalid date format",
                    "Invalid date value",
                ]
            ):
                return err_text
            for e_type, msg in MESSAGES.items():
                if isinstance(e, e_type):
                    return msg
            return f"Unexpected error: {e}"

    return inner
