
def color_string(string, color):
    color_map = {
        'black': '90m',
        'red': '31m',
        'green': '32m',
        'blue': '34m',
        'white': '7;15m',
        'colorless': '37m',
        'gold': '33m',
    }

    return '\033[{color_code}{string}\033[0m'.format(color_code=color_map[color], string=string)
    # return '\033[1;{color_code}m{string}\033[1;m'.format(color_code=color_map[color], string=string)
