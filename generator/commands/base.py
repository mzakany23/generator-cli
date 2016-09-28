import os

"""The base command."""

class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
		self.options = options
		self.args = args
		self.kwargs = kwargs

		self.project = options['<project>']
		self.name = options['<name>']
		self.path = options['<path>'] or os.path.expanduser("~") + '/Desktop'
		
    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
