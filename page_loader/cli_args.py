import argparse
from os import getcwd


def parse():
    parser = argparse.ArgumentParser(
        description='Downloads html page with all its resources'
    )
    parser.add_argument(
        '-o',
        '--output',
        help='output folder path',
        default=getcwd()
    )
    parser.add_argument('url')
    return parser.parse_args()
