"""The generate subcommand."""

from json import dumps

from .base import Base

from lib import make_commands

class SubCommands(Base):
	"""Sub Commands"""

	def run(self):
		cmd = make_commands.get_command(self.options)
		make_commands.run(cmd)
		

		
	
    
    	
        
