class FatalError(Exception):
    """Exception for fatal errors that should terminate execution."""

    def __init__(self, message: str = "Fatal Error") -> None:
        super().__init__(message)


class MildError(Exception):
    """Exception for non-fatal errors that allow execution to continue."""

    def __init__(self, message: str = "Mild Error") -> None:
        super().__init__(message)
