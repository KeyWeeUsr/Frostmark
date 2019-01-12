'''
Module for interfacing with the package via python command::

    python -m frostmark
'''
from frostmark.parser import PARSER


PARSER.set_defaults(type='main')
PARSER.console_parser.set_defaults(type='console')
PARSER.gui_parser.set_defaults(type='gui')


if __name__ == '__main__':
    MAIN_PARSER = PARSER.parse_args()

    if MAIN_PARSER.type == 'main':
        PARSER.print_help()
        exit()
    elif MAIN_PARSER.type == 'console':
        from frostmark.core.console import Console as Client
    elif MAIN_PARSER.type == 'gui':
        from frostmark.core.gui import GUI as Client
    Client(**vars(MAIN_PARSER)).run()
