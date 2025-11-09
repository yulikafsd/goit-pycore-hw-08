class ValidationError(Exception):
    def __init__(self, message):
        self.message = f'{"-"*10} {message} {"-"*10}'
        super().__init__(self.message)
