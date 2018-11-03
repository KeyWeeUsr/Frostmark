class Console(object):
    logo = [
        '╔═╗┬─┐┌─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐┬┌─',
        '╠╣ ├┬┘│ │└─┐ │ │││├─┤├┬┘├┴┐',
        '╚  ┴└─└─┘└─┘ ┴ ┴ ┴┴ ┴┴└─┴ ┴'
    ]

    def __init__(self, **kwargs):
        self.parameters = kwargs

    def run(self, *args, **kwargs):
        print('\n'.join(self.logo))
        print("Use '-h' or '--help' for more instructions.")
