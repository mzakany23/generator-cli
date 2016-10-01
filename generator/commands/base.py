import os

"""The base command."""

class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
		self.options = options
		self.args = args
		self.kwargs = kwargs
		
		self.project = options['project-type']
		self.name = options['site-name']
		
		if options['path'] and os.path.isdir(os.path.abspath(options['path'])):
			self.path = os.path.abspath(options['path'])
			options['path'] = self.path
		else:
			self.path = os.path.expanduser("~") + '/Desktop'
		
    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
