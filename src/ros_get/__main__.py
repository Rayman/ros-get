#!/usr/bin/env python
from __future__ import print_function

import logging.config
from argparse import ArgumentParser

from ros_get.commands import install, update, upgrade, remove

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format':
                "%(log_color)s[%(levelname)s] %(name)s: %(message)s",
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        'vcstool.executor': {
            'level': 'INFO',
        }

    },
    'root': {
        'handlers': ['stream'],
        'level': 'INFO',
    },
})


def not_implemented():
    raise NotImplementedError()


def main():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')

    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('install', help='install packages')
    subparser.set_defaults(func=install)
    subparser.add_argument('pkgs', nargs='+', metavar='pkg')

    subparser = subparsers.add_parser('update', help='update list of available packages')
    subparser.set_defaults(func=update)

    subparser = subparsers.add_parser('upgrade', help='upgrade the workspace by installing/upgrading packages')
    subparser.set_defaults(func=upgrade)

    subparser = subparsers.add_parser('remove', help='remove packages')
    subparser.set_defaults(func=remove)
    subparser.add_argument('pkgs', nargs='+', metavar='pkg')

    subparser = subparsers.add_parser('autoremove', help='remove automatically all unused packages')
    subparser.set_defaults(func=not_implemented)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    func = args.func
    del args.func
    exit(func(**vars(args)))


if __name__ == '__main__':
    main()
