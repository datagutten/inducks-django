import re


def replace_slash(code):
    if type(code) is int:
        return code
    return re.sub(r'([a-z]+)/(.+)', r'\1-\2', code).replace('/', '!')


def replace_dash(code):
    return re.sub(r'([a-z]+)-(.+)', r'\1/\2', code).replace('!', '/')


def clean_chars(string: str):
    if type(string) is not str:
        return string
    try:
        return int(string)
    except ValueError:
        pass
    string = re.sub(r'[ÀÁÂÃÄÅ]', "A", string)
    string = re.sub(r'[àáâãäå]', "a", string)
    string = re.sub(r'[ÈÉÊË]', "E", string)
    string = re.sub(r'[ό]', 'o', string, re.IGNORECASE)
    # //.... all the rest
    # string = re.sub(r'[^a-z0-9]', '', string, flags=re.IGNORECASE)  # final clean up
    return string.lower()
