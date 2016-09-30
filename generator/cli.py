"""
generator

Usage:
  generator g <project> <name>
  generator g <project> <name> -p <path>
  generator make:django route products:create
  
Options:
  -d --directory                    Specify directory.
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  generator g project django
  generator make:djangoapi products -d ~/Desktop

Help:
  <project> types:
    - django
    - django-api
    - riot-webpack
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
  
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
