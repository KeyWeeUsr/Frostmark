'''
Module for console interface.
'''
# pylint: disable=too-few-public-methods


class Console:
    '''
    Console object used if console interface is chosen.
    '''

    logo = [
        '╔═╗┬─┐┌─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐┬┌─',
        '╠╣ ├┬┘│ │└─┐ │ │││├─┤├┬┘├┴┐',
        '╚  ┴└─└─┘└─┘ ┴ ┴ ┴┴ ┴┴└─┴ ┴'
    ]

    def __init__(self, **kwargs):
        self.parameters = kwargs

    def run(self, *_, **__):
        '''
        Main function in case of 'console' argument without specific
        parameters is supplied.
        '''

        print('\n'.join(self.logo))
        print("Use '-h' or '--help' for more instructions.")
