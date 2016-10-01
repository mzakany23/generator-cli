"""
generator

Usage:
  generator <cmd> <project>:<name>
  generator <cmd> <project>:<name> -p <path>
  generator <sub-cmd>:<project> <type> <controller>:<action>
  
Options:
  -d --directory                    Specify directory.
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  generator new django:mysite
  generator new django:mysite -p /path/to/dir
  generator make:django route products:create

Help:
  <project> types:
    - django
    - django-api
    - riot-webpack
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

from lib import cli_cmds

def main():
    """Main CLI entrypoint."""
    import commands

    options = docopt(__doc__, version=VERSION)

    cmds = cli_cmds.command_lookup(options)
    
    def get_commands(type):
      module = getattr(commands, type)
      members = getmembers(module, isclass)
      
      def inner(cls):
        for member in members:
          if member[0] == cls:
            return member[1]
      return inner
      
    if cmds['cmd']['type']['new']:
      commands = get_commands('new')
      command = commands('Generate')
    
    elif cmds['cmd']['type']['make']['route']:
      commands = get_commands('make')
      command = commands('SubCommands')
    command(cmds).run()
      
