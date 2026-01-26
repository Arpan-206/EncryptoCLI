from typing import Union

import util.exceptions as exceptions
from termcolor import colored


def handle_error(
    e: Union[exceptions.FatalError, exceptions.MildError, Exception],
) -> None:
    """Handle and display errors with appropriate coloring."""
    if isinstance(e, exceptions.FatalError):
        print(colored(str(e), "red"))
    elif isinstance(e, exceptions.MildError):
        print(colored(str(e), "yellow"))
