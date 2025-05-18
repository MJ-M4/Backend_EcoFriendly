class DataFetchError(Exception):
    def __init__(self, message="Data fetch error"):
        self.message = message
        super().__init__(self.message)
