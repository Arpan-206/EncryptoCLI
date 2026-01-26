class FatalError(Exception):
    """Exception for fatal errors that should terminate execution.

    Attributes:
        message: The error message.
    """

    def __init__(self, message: str = "Fatal Error") -> None:
        """Initialize FatalError exception.

        Args:
            message: The error message (defaults to "Fatal Error").

        Returns:
            None
        """
        super().__init__(message)


class MildError(Exception):
    """Exception for non-fatal errors that allow execution to continue.

    Attributes:
        message: The error message.
    """

    def __init__(self, message: str = "Mild Error") -> None:
        """Initialize MildError exception.

        Args:
            message: The error message (defaults to "Mild Error").

        Returns:
            None
        """
        super().__init__(message)
