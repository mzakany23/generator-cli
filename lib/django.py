from lib.util import *
from lib.templates import t_gen

class Django(object):
	def __init__(self,name,path,type):
		self.name = name 
		self.path = path 
		self.type = type
		
		# files
		self.settings_file = '../templates/django/settings/settings.py'
		self.new_settings_file = "%s/%s/%s/%s/settings.py" % (path,name,name,name)

		# cli directory lookup
		self.reqire_dir = {
			'development' : "%s/templates/django/requirements/development.txt" % get_rd(),
			'development-test' : "%s/templates/django/requirements/development-test.txt" % get_rd()
		}

		self.settings_dir = {
			'settings' : "%s/templates/django/settings" % get_rd()
		}

		self.ctx = {
			'settings' : {
				'modules' : ['home']
			}
		}

		# django app directory lookup
		self.app_paths = {
			'venv' : path,
			'settings' : "%s/%s/%s/" % (path,name,name),
			'root' : "%s/%s/" % (path,name),
			'manage.py' : "%s/%s/%s" % (path,name,name)
		}

	
	def make_virtual_env(self):
		run('virtualenv %s' % self.name)

	def install_requirements(self):
		raise NotImplementedError('You must implement the install_requirements() method yourself!')

	def setup(self):
		raise NotImplementedError('You must implement the setup() method yourself!')

	def make_static_files(self):
		touch('.gitignore')
		touch('static/templates/home/index.html')
		touch('%s/api/__init__.py' % self.name)

	def make_static_dirs(self):
		mkdir('docs')
		mkdir('logs')
		mkdir('tests')
		mkdir('static/static/assets/')
		mkdir('static/static/assets/js')
		mkdir('static/static/assets/css')
		mkdir('static/static/assets/img')
		mkdir('static/media')
		mkdir('static/root')
		mkdir('static/templates/layouts/partials')
		
	def setup_migrations(self):
		run('python manage.py createmigrations')
		run('python manage.py migrate')	

	
	def create_project(self):
		run('django-admin.py startproject %s' % self.name)

	def make_settings_file(self):
		sfile = make_ctx_file(
			self.settings_dir['settings'],
			'settings.py',
			self.ctx['settings']
		)
		
		settings = "%s/settings.py" % self.app_paths['settings']

		create_file(settings,sfile)

	def install_requirements(self,key):
		with virtualenv('%s/bin' % self.name):
			run_install(self.reqire_dir[key])	

class DjangoMonolith(Django):
	def __init__(self,name,path,type):
		Django.__init__(self,name,path,type)

	def setup(self):
		cd(self.path)	
		self.make_virtual_env()
		self.install_requirements('development-test')

		cd(self.name)
		self.make_static_dirs()
		self.make_static_files()
		self.create_project()
		self.make_settings_file()

		cd(self.app_paths['manage.py'])
		self.setup_migrations()

		


	