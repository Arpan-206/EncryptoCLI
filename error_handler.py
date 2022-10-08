
import util.exceptions as exceptions
from termcolor import colored

def handle_error(e):
    if( isinstance(e, exceptions.FatalError) ):
        print( colored(str(e), 'red') )
    elif( isinstance(e, exceptions.MildError) ):
        print( colored(str(e), 'yellow') )
    else:
        print(e)