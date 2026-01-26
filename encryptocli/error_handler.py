import encryptocli.util.exceptions as exceptions
from termcolor import colored


def handle_error(
    e: exceptions.FatalError | exceptions.MildError | Exception,
) -> None:
    """Handle and display errors with appropriate coloring.

    Args:
        e: The exception to handle and display.

    Returns:
        None
    """
    if isinstance(e, exceptions.FatalError):
        print(colored(str(e), "red"))
    elif isinstance(e, exceptions.MildError):
        print(colored(str(e), "yellow"))
