#!/usr/bin/env python
import logging
import sys

from page_loader import cli_args
from page_loader import page


def main():
    try:
        args = cli_args.parse()
        path = page.download(args.url, args.output)
        print(path)
    except Exception as error:
        logging.error(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
