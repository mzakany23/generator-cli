"""Tests for our main generator CLI module."""

import unittest
import sys 
sys.path.append('../')
from lib.cli import * 

class TestHelp(unittest.TestCase):
	def setUp(self):
		self.output = {
			'-p': False,
			'<name>': None,
			'<path>': None,
			'<project>': None,
			'g': False,
			'make:django': True,
			'products:create': True,
			'route': True
		}

		self.test_output = {
			'name' : "{0}.views as {0}_views".format(controller),
	 		'url' : "url(r'^/{0}$', {0}_views.create,name='{1}'),".format(action,controller)
		}

		def is_make_command(c):
			if c[0] == 'make':
				return c

		def process_command(command):
			return cli.lookup['make']['django']['routes']['create']('products','')

		for k in output:
			subcommand = k.split(':')

			if is_make_command(subcommand):
				process_command(subcommand)


if __name__ == '__main__':
	unittest.main()

