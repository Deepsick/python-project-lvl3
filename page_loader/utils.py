import re
from os.path import splitext


def format(file_name, replacer='-'):
    return re.sub(r'[^a-zA-Z0-9]', replacer, file_name)


def get_base_name(url):
    return format(url.split('://')[1])


def build_name(base, postfix):
    return f'{base}{postfix}'


def build_resource_name(url):
    root, ext = splitext(url)
    postfix = ext if ext else '.html'
    return build_name(get_base_name(root), postfix)
