import os
from os import listdir
from os.path import isfile,join,basename
from subprocess import call,check_call,Popen
from functools import wraps
from shutil import copyfile
from lib.templates import t_gen

class virtualenv:
	def __init__(self,bin_path):
		self.fp = "%s/activate_this.py" % bin_path
		
	def __enter__(self):
		execfile(self.fp, dict(__file__=self.fp))
		return self

	def __exit__(self, type, value, traceback):
		return self

def error(str,type=None):
	exp = type if type else Exception
	raise exp(str)

def expand_path(path):
	if path[0] == '~':
		path = "%s/%s" % (os.environ['HOME'],basename(path))
	return path

def cd(path):
	if path[0] == '~': 
		sp = path[2:]
		path = "%s%s" % (expand_path('~/'),sp)
	else: 
		path = "%s" % path
		
	os.chdir(path) if os.path.exists(path) else error('%s Path doesnt exist' % path,type=OSError)
			
def ls():
	print [f for f in listdir('.')]

def mv(op,np):
	op = get_path(op)

	if isfile(op) and isfile(np):
		os.copyfile(op,np)

def get_rd():
	'''get the project base path i.e. /path/to/generator-cli'''
	path = os.path.dirname(os.path.realpath(__file__)).split('/')
	i,j = 0,0
	while i < len(path):
		item = path[i]
		if item == 'generator-cli':
			j = i
		i += 1
	return '/'.join(path[0:j+1])

def run(cmd):
	os.system(cmd)

def get_path(path):
	dp = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[1:-1])
	rp = os.path.relpath(path).replace('../','')
	fp = "/%s/%s" % (dp,rp)
	return fp

def file_contents_to_array(fp):
	cts = []
	with open(fp,'r') as f:
		cts = [line.rstrip() for line in f.readlines()]
	return cts

def run_install(wf):	
	fc = file_contents_to_array(wf)
	def fn(pkg): run('pip install %s' % pkg)
	map(fn,fc)

def mkdir(directory):
	os.makedirs(directory) if not os.path.exists(directory) else error('%s exists' % directory,type=Exception)

def fcombine(path,fname,ctx=None):
	'''
		path to directory
		filename in that directory
		context to put in file 
	'''
	template = t_gen(path)
	return template(fname,ctx)
	
def create_file(fpath,sfile):
	with open(fpath, 'w') as f:
			f.write(sfile)

def touch(path):
	basedir = os.path.dirname(path)
	if not os.path.exists(basedir) and basedir:
	    mkdir(basedir)

	with open(path, 'a'):
		os.utime(path, None)


