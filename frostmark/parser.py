'''
Module for parsing arguments from console.
'''

from argparse import ArgumentParser, Action

from frostmark import VERSION, __name__ as name
from frostmark.common import fetch_bookmark_tree, print_bookmark_tree
from frostmark.editor import Editor
from frostmark.importer import Importer
from frostmark.exporter import Exporter
from frostmark.profiles import print_profiles
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

# add optional argument for console parser
PARSER.console_parser.add_argument(
    '-l', '--list-bookmarks',
    help='show all available bookmarks as a tree',
    required=False, nargs=0,

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: print_bookmark_tree(
            fetch_bookmark_tree()
        )
    )
)

PARSER.console_parser.add_argument(
    '-p', '--list-profiles',
    help='import bookmarks from a browser profile',
    required=False, nargs=1,
    metavar=('BROWSER', ),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: print_profiles(
            kwargs['arg_values'][0]
        )
    )
)

PARSER.console_parser.add_argument(
    '-i', '--import-bookmarks',
    help='import bookmarks from a browser profile',
    required=False, nargs='+',
    metavar=('BROWSER', 'PROFILE'),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: [
            Importer(
                kwargs['arg_values'][0]
            ).import_from(val)
            for val in kwargs['arg_values'][1:]
        ]
    )
)

PARSER.console_parser.add_argument(
    '-x', '--export-bookmarks',
    help='export bookmarks to an HTML format',
    required=False, nargs=1,
    metavar=('PATH', ),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Exporter().export_to(
            path=kwargs['arg_values'][0]
        )
    )
)

PARSER.console_parser.add_argument(
    '-cpf', '--change-parent-folder',
    help='change parent for a folder',
    required=False, nargs=2,
    metavar=('FOLDER_ID', 'PARENT_ID'),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Editor.change_parent_folder(
            folder_id=int(kwargs['arg_values'][0]),
            parent_id=int(kwargs['arg_values'][1])
        )
    )
)

PARSER.console_parser.add_argument(
    '-cpb', '--change-parent-bookmark',
    help='change parent for a bookmark',
    required=False, nargs=2,
    metavar=('BOOKMARK_ID', 'PARENT_ID'),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Editor.change_parent_bookmark(
            bookmark_id=int(kwargs['arg_values'][0]),
            parent_id=int(kwargs['arg_values'][1])
        )
    )
)

PARSER.console_parser.add_argument(
    '-rf', '--rename-folder',
    help='rename folder',
    required=False, nargs=2,
    metavar=('FOLDER_ID', 'NAME'),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Editor.rename_folder(
            folder_id=int(kwargs['arg_values'][0]),
            name=kwargs['arg_values'][1]
        )
    )
)

PARSER.console_parser.add_argument(
    '-rb', '--rename-bookmark',
    help='rename bookmark',
    required=False, nargs=2,
    metavar=('BOOKMARK_ID', 'NAME'),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Editor.rename_bookmark(
            bookmark_id=int(kwargs['arg_values'][0]),
            name=kwargs['arg_values'][1]
        )
    )
)

PARSER.console_parser.add_argument(
    '-cbu', '--change-bookmark-url',
    help='change url for a bookmark',
    required=False, nargs=2,
    metavar=('BOOKMARK_ID', 'URL'),

    # pylint: disable=unnecessary-lambda
    action=lambda *args, **kwargs: ExecuteAction(
        *args, **kwargs,
        func=lambda *args, **kwargs: Editor.change_bookmark_url(
            bookmark_id=int(kwargs['arg_values'][0]),
            url=kwargs['arg_values'][1]
        )
    )
)
