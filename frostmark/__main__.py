'''
Module for interfacing with the package via python command::

    python -m frostmark
'''
from ensure import ensure_annotations
from frostmark.parser import PARSER


PARSER.set_defaults(type='main')
PARSER.console_parser.set_defaults(type='console')
PARSER.gui_parser.set_defaults(type='gui')


@ensure_annotations
def main(name: str = '__main__'):
    '''
    Main function for module entrypoint.
    '''

    if name != '__main__':
        return

    main_parser = PARSER.parse_args()

    if main_parser.type == 'main':
        PARSER.print_help()
        exit()
    elif main_parser.type == 'console':
        from frostmark.core.console import Console as Client
    elif main_parser.type == 'gui':
        from frostmark.core.gui import GUI as Client
    Client(**vars(main_parser)).run()


main(__name__)
