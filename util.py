
def color_string(string, color):
    color_map = {
        'black':    30,
        'red':      31,
        'green':    32,
        'blue':     34,
        'white':    37,
    }

    return '\033[1;{color_code}m{string}\033[1;m'.format(color_code=color_map.get(color, 37), string=string)
