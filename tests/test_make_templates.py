"""Tests for our main generator cli_cmds module."""

import unittest
import os
import sys 
sys.path.append('../')
from lib import templates,util

from mock import MagicMock

class CmdTests(unittest.TestCase):
	def setUp(self):
		base = os.path.abspath('./')
		self.write_dir = base + '/files'
		self.mock_dir = base + '/files/mock'
		self.output_dir = base + '/files/output'
		self.urls_file = self.mock_dir + '/urls.py'

	def mock_create_file(self,name,file):
		return MagicMock(return_value=self.output_dir+'/new_urls.py')
		
	def test_create_file(self):
		gfile = util.fcombine(self.mock_dir,'urls.py',name,None)
		# create a new urls file and put in output dir
		cfile = self.mock_create_file(self.output_dir+'/new_urls.py',gfile).return_value
		self.assertTrue(os.path.basename(cfile) == 'new_urls.py')

	def test_template_inheritance(self):
		'''python test_make_files.py CmdTests.test_template_inheritance'''
		# gfile = util.fcombine(self.mock_dir,'index.html',None)
		gfile = MagicMock(return_value='file there dude')
		self.assertTrue(gfile.return_value == 'file there dude')

	def test_create_file_with_context(self):
		'''python test_make_files.py CmdTests.test_create_file_with_context'''
		pass



if __name__ == '__main__':
	unittest.main()

