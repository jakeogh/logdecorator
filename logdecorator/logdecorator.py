# DEBUG      Detailed information, typically of interest only when diagnosing problems.
# INFO       Confirmation that things are working as expected.
# WARNING    An indication that something unexpected happened, or indicative of some problem in the near future
#               (e.g. ‘disk space low’). The software is still working as expected.
# ERROR      Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL   A serious error, indicating that the program itself may be unable to continue running.

import colorama
from colorama import Fore

import logging

__version__ = "0.0.1"

class logmaker():
    def __init__(self, output_format, name, level):
        self.logger = logging.getLogger(name)
        self.logger_ch = logging.StreamHandler()
        self.formatter = logging.Formatter(output_format)
        self.logger_ch.setFormatter(self.formatter)
        self.logger.addHandler(self.logger_ch)
        self.logger.setLevel(level)


# http://stackoverflow.com/questions/10973362/python-logging-function-name-file-name-line-number-using-a-single-file
FORMAT = "%(levelname)-5s %(lineno)4s %(filename)-18s:%(funcName)-13s : %(message)s" + Fore.RESET
QUIET_FORMAT = "%(message)s" + Fore.RESET

FORMATTER = logging.Formatter(FORMAT)
QUIET_FORMATTER = logging.Formatter(QUIET_FORMAT)

#http://docs.python.org/3/howto/logging.html
LOG_LEVELS = {
'CRITICAL':logging.CRITICAL,    # 50
'ERROR':   logging.ERROR,       # 40
'WARNING': logging.WARNING,     # 30    #python default level
'INFO':    logging.INFO,        # 20
'DEBUG':   logging.DEBUG        # 10
}

#logging.basicConfig(format=FORMAT, level=LOG_LEVELS['WARNING'])

# Logger.setLevel() specifies the lowest-severity log message a logger will
#   handle, where debug is the lowest built-in severity level and critical is
#   the highest built-in severity. If the severity level is INFO, the logger
#   will handle only INFO, WARNING, ERROR, and CRITICAL messages and will
#   ignore DEBUG messages.

# Logger.exception() creates a log message similar to Logger.error(). The
#   difference is that Logger.exception() dumps a stack trace along with it.
#   Call this method only from an exception handler.

# Logger.log() takes a log level as an explicit argument. This is a little more
#   verbose for logging messages than using the log level convenience methods
#   listed above, but this is how to log at custom log levels.


from functools import wraps
from functools import partial
import sys
import pprint
import traceback
import inspect

def get_parent_function():
    return inspect.stack()[2][3]

def print_traceback():
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb)
    del tb

log_prefix_logger = logmaker(output_format=FORMAT, name="logging_debug3", level=LOG_LEVELS['DEBUG'])

def log_prefix(func=None, *, prefix='', return_status='', log_level='DEBUG', show_args=True):
    if func is None:
        return partial(log_prefix, prefix=prefix, return_status=return_status, log_level=log_level, show_args=show_args)
    msg = prefix + '[' + func.__qualname__ + '()]'

    @wraps(func)
    def FUNCTION_CALL(*args, **kwargs):
        parent = get_parent_function()
        args_list = []
        for arg in args:
            if isinstance(arg, bytes):
                arg = arg.decode(encoding='UTF-8')
                args_list.append(arg)
            elif isinstance(arg, str): #unicode
                args_list.append(arg)
            else:
                try:
                    args_list.append(pprint.pformat(arg))
                except:
                    args_list.append("unconvertable thing:" + str(type(arg)))

        if show_args:
            args_output_string = ' '.join(pprint.pformat(args_list).split("\n"))
            kwargs_output_string = ' '.join(pprint.pformat(kwargs).split("\n"))
        else:
            args_output_string = '(args supressed) '
            kwargs_output_string = '(kwargs_supressed)'

        output_string = msg + ' caller: ' + parent + '()' + ' args:' + args_output_string + kwargs_output_string

        if log_level == 'DEBUG':
            log_prefix_logger.logger.debug(Fore.GREEN + output_string)
        elif log_level == 'INFO':
            log_prefix_logger.logger.info(Fore.WHITE + output_string)
        elif log_level == 'WARNING':
            log_prefix_logger.logger.warning(Fore.YELLOW + output_string)
        elif log_level == 'ERROR':
            log_prefix_logger.logger.error(Fore.RED + output_string)
        elif log_level == 'CRITICAL':
            log_prefix_logger.logger.critical(Fore.RED + output_string)
        else:
            log_prefix_logger.logger.critical("UNKNOWN LOG LEVEL:", log_level)
            quit(1)

        answer = func(*args, **kwargs)
        if answer == False:
            log_prefix_logger.logger.debug(Fore.RED + func.__name__ + " returned False")
        else:
            if return_status == True:
                log_prefix_logger.logger.debug(Fore.YELLOW + func.__name__ + " OK")
        return answer

    return FUNCTION_CALL

def main():
    pass
#    logger.info('logdecorator.py:main()')


# Fore.BLACK
# Fore.BLUE
# Fore.CYAN
# Fore.GREEN
# Fore.MAGENTA
# Fore.RED
# Fore.RESET
# Fore.WHITE
# Fore.YELLOW

