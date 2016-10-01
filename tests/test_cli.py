"""Tests for our main generator cli_cmds module."""

import unittest
import sys 
sys.path.append('../')

from lib import cli_cmds

class CmdTests(unittest.TestCase):
	def setUp(self):
		self.new_command = {
			'-p': '~/Desktop',
			'<cmd>': 'new',
			'<controller>:<action>': None,
			'<path>': None,
			'<project>:<name>': 'django:mysite',
			'<sub-cmd>:<project>': None,
			'<type>': None
		}

		self.make_command = {
			'-p': False,
			'<cmd>': None,
			'<controller>:<action>': 'products:new',
			'<path>': None,
			'<project>:<name>': None,
			'<sub-cmd>:<project>': 'make:django',
			'<type>': 'route'
		}


	def is_make_command(self,c):
		if c[0] == 'make':
			return c

	def test_new_command(self):
		''' generator new django:mysite '''
		cmds = cli_cmds.command_lookup(self.new_command)
		self.assertTrue(cmds['cmd']['type']['new'])
		
	def test_subcommand(self):
		cmds = cli_cmds.command_lookup(self.make_command)
		self.assertTrue(cmds['cmd']['type']['make']['controller'] == 'products')

	def test_make_new_django_app(self):
		self.assertTrue(cli_cmds.lookup()['new']('myproject','django')[0] == 'django')


if __name__ == '__main__':
	unittest.main()

