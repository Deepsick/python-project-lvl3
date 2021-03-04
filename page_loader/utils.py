import re
from urllib.parse import urlparse
from os.path import splitext


def format(file_name, replacer='-'):
    return re.sub(r'[^a-zA-Z0-9]', replacer, file_name)


def build_name(url, is_folder=False):
    parsed_url = urlparse(url)
    path, ext = splitext(parsed_url.path)
    full_name = f"{parsed_url.netloc}{path}"
    formated_name = format(full_name)
    postfix = ext if ext else '.html'
    postfix = '_files' if is_folder else postfix
    return f"{formated_name}{postfix}"
