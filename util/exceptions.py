
class FatalError(Exception):

    def __init__ (self, message="Fatal Error"):
        super().__init__(message)

class MildError(Exception):

    def __init__(self, message="Mild Error"):
        super().__init__(message)