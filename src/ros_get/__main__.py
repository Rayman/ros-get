#!/usr/bin/env python
from __future__ import print_function

import logging.config
from argparse import ArgumentParser

from ros_get.commands import install, update, list_installed, remove
from ros_get.workspace import create, switch, save, list_workspaces, locate

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(levelname)s] %(name)s: %(message)s",
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

    subparser = subparsers.add_parser('update', help='update all packages in the workspace to the latest version')
    subparser.set_defaults(func=update)

    subparser = subparsers.add_parser('list', help='list all installed packages')
    subparser.set_defaults(func=list_installed)

    subparser = subparsers.add_parser('remove', help='remove packages')
    subparser.set_defaults(func=remove)
    subparser.add_argument('pkgs', nargs='+', metavar='pkg')

    subparser = subparsers.add_parser('autoremove', help='remove automatically all unused packages')
    subparser.set_defaults(func=not_implemented)

    # workspace commands
    subparser = subparsers.add_parser('ws-create', help='create a new workspace')
    subparser.set_defaults(func=create)
    subparser.add_argument('dir')
    subparser.add_argument(
        'extend_path',
        metavar='extend',
        help='Explicitly extend the result-space of another catkin workspace, '
        'overriding the value of $CMAKE_PREFIX_PATH.')
    subparser.add_argument(
        '--name', help='give a name to the workspace, if not given, the name '
        'will be inferred by the directory name')

    subparser = subparsers.add_parser('ws-switch', help='switch to a workspace')
    subparser.set_defaults(func=switch)
    subparser.add_argument('name')

    subparser = subparsers.add_parser('ws-save', help='Saves the current workspace')
    subparser.set_defaults(func=save)
    subparser.add_argument('dir')
    subparser.add_argument(
        '--name', help='give a name to the workspace, if not given, the name will be inferred by the directory name')

    subparser = subparsers.add_parser('ws-list', help='list all saved workspaces')
    subparser.set_defaults(func=list_workspaces)

    subparser = subparsers.add_parser('ws-locate', help='prints the path to the current workspace')
    subparser.set_defaults(func=locate)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    func = args.func
    del args.func
    exit(func(**vars(args)))


if __name__ == '__main__':
    main()
