from argparse import ArgumentParser, Action
from pprint import pprint

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
    def __init__(self, func=None, func_args=(), func_kwargs={}, *a, **kw):
        super(ExecuteAction, self).__init__(*a, **kw)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def __call__(self, parser, namespace, values, option_string=None):
        self.func_kwargs['arg_values'] = values
        self.func(*self.func_args, **self.func_kwargs)
        exit()


class FrostmarkArgumentParser(ArgumentParser):
    def print_help(self, *args, **kwargs):
        print('\n'.join(Console.logo))
        super(FrostmarkArgumentParser, self).print_help(*args, **kwargs)


# create main parser
Parser = FrostmarkArgumentParser(
    prog=name,
    epilog='Epilog',
    add_help=True
)
Parser.add_argument(
    '-V', '--version',
    action='version',
    version='%(prog)s %(ver)s' % {
        'prog': Parser.prog, 'ver': VERSION
    }
)

# create subparsers for main parser
subparsers = Parser.add_subparsers()

# add positional argument for main parser
Parser.console_parser = subparsers.add_parser('console')
Parser.gui_parser = subparsers.add_parser('gui')
