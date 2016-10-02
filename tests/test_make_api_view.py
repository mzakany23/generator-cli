"""Tests for our main generator cli_cmds module."""

import unittest
import os
import sys 
sys.path.append('../')
from lib import templates,util

from mock import MagicMock

class APIViewTests(unittest.TestCase):
	def setUp(self):
		self.project_path = os.path.abspath('./test_make_commands')

	def test_make_api_app(self):
		'''python test_make_api_view.py APIViewTests.test_make_api_app'''
		util.cd(self.project_path)
		util.ls()


if __name__ == '__main__':
	unittest.main()

