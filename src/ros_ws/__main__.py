import os
import sys
from argparse import ArgumentParser, Action, SUPPRESS

from argcomplete import autocomplete


class VersionAction(Action):
    """
    Custom VersionAction that prints the version of this package
    """

    def __init__(self,
                 option_strings,
                 dest=SUPPRESS,
                 default=SUPPRESS,
                 help="show program's version number and exit"):
        super(VersionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        from . import __version__
        formatter = parser._get_formatter()
        python_version = '.'.join(map(str, sys.version_info[:2]))
        formatter.add_text('%(prog)s version ' + __version__ + ' (python ' + python_version + ')')
        parser.exit(message=formatter.format_help())


def parse_args(argv):
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--version', action=VersionAction)

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # workspace commands
    subparser = subparsers.add_parser(
        'create',
        help='create a new workspace',
        description='Create a new colcon workspace where the packages are managed by ros-ws')
    subparser.set_defaults(func='create')
    subparser.add_argument(
        'extend_path',
        metavar='extend',
        help='Explicitly extend the result-space of another workspace. Example: /opt/ros/humble')
    subparser.add_argument(
        '--dir',
        default=os.getcwd(),
        help='The directory to create the workspace in. Defaults to the current working directory')
    subparser.add_argument(
        '--name',
        help='give a name to the workspace, if not given, the name will be inferred by the directory name')

    subparser = subparsers.add_parser('switch', help='switch to a workspace')
    subparser.set_defaults(func='switch')
    subparser.add_argument('name')

    subparser = subparsers.add_parser('save', help='Saves the current workspace')
    subparser.set_defaults(func='save')
    subparser.add_argument('dir')
    subparser.add_argument(
        '--name', help='give a name to the workspace, if not given, the name will be inferred by the directory name')

    subparser = subparsers.add_parser('list', help='list all saved workspaces')
    subparser.set_defaults(func='list_workspaces')

    subparser = subparsers.add_parser('locate', help='prints the path to the current workspace')
    subparser.set_defaults(func='locate')

    subparser = subparsers.add_parser('name', help='prints the name of the current workspace')
    subparser.set_defaults(func='name')

    autocomplete(parser)
    args = parser.parse_args(argv)

    # computation has to be avoided before the 'autocomplete(parser)' call

    import logging.config
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
        'root': {
            'handlers': ['stream'],
            'level': 'INFO',
        },
    })

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # remove func from the namespace
    func = args.func
    del args.func
    del args.command

    return func, args


def main():
    from . import (create, switch, save, list_workspaces, locate, name)

    func, args = parse_args(sys.argv[1:])
    # execute the function given in 'func'
    func = {
        'create': create,
        'switch': switch,
        'save': save,
        'list_workspaces': list_workspaces,
        'locate': locate,
        'name': name,
    }[func]
    return func(**vars(args))


if __name__ == '__main__':
    exit(main())
