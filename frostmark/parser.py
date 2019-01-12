'''
Module for parsing arguments from console.
'''

from argparse import ArgumentParser, Action

from frostmark import VERSION, __name__ as name
from frostmark.core.console import Console


class ExecuteAction(Action):
    '''ArgumentParser action for add_argument(action=...)

    Executes a function and its args + kwargs passed as
    the __init__ arguments:

      * func
      * func_args
      * func_kwargs

    together with argument values inserted into func_kwargs
    as 'arg_values' and exits immediately.
    '''
    # pylint: disable=too-few-public-methods

    def __init__(self, *a, func=None, func_args=(), func_kwargs={}, **kw):
        # pylint: disable=dangerous-default-value

        super(ExecuteAction, self).__init__(*a, **kw)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def __call__(self, parser, namespace, values, option_string=None):
        self.func_kwargs['arg_values'] = values
        self.func(*self.func_args, **self.func_kwargs)
        exit()


class FrostmarkArgumentParser(ArgumentParser):
    '''
    Inheriting from `ArgumentParser` to print custom print message.
    '''
    # pylint: disable=too-few-public-methods

    def print_help(self, *args, **kwargs):
        # pylint: disable=arguments-differ
        print('\n'.join(Console.logo))
        super(FrostmarkArgumentParser, self).print_help(*args, **kwargs)


# create main parser
PARSER = FrostmarkArgumentParser(
    prog=name,
    epilog='Epilog',
    add_help=True
)
PARSER.add_argument(
    '-V', '--version',
    action='version',
    version='%(prog)s %(ver)s' % {
        'prog': PARSER.prog, 'ver': VERSION
    }
)

# create subparsers for main parser
SUBPARSERS = PARSER.add_subparsers()

# add positional argument for main parser
# pylint: disable=attribute-defined-outside-init
PARSER.console_parser = SUBPARSERS.add_parser('console')
PARSER.gui_parser = SUBPARSERS.add_parser('gui')
