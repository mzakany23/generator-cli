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
		self.templates_dir = {
			'home' : "%s/templates/django/templates/home/index.html" % get_rd(),
			'base' : "%s/templates/django/templates/layouts/base.html" % get_rd()
		}
		self.reqire_dir = {
			'development' : "%s/templates/django/requirements/development.txt" % get_rd(),
			'development-test' : "%s/templates/django/requirements/development-test.txt" % get_rd()
		}

		self.settings_dir = {
			'settings_dir' : "%s/templates/django/settings" % get_rd(),
			'settings' : "%s/templates/django/settings/settings.py" % get_rd(),
			'env' : "%s/templates/django/settings/env.py" % get_rd()
		}

		self.urls_dir = {
			'urls' : "%s/templates/django/urls" % get_rd()
		}

		self.views_dir = {
			'home' : "%s/templates/django/views/home/views.py" % get_rd()
		}

		self.ctx = {
			'settings' : {
				'modules' : ['home']
			}
		}

		# django app directory lookup
		self.app_paths = {
			'app' : "%s/%s" % (path,name),
			'venv' : path,
			'settings' : "%s/%s/%s/" % (path,name,name),
			'urls' : "%s/%s/%s/" % (path,name,name),
			'root' : "%s/%s/" % (path,name),
			'manage.py' : "%s/%s/%s" % (path,name,name),
		}

	
	def make_virtual_env(self):
		run('virtualenv %s' % self.name)

	def setup(self):
		raise NotImplementedError('You must implement the setup() method yourself!')

	def make_static_files(self):
		touch('.gitignore')
		# touch('%s/home/views.py' % self.name)
		touch('%s/home/__init__.py' % self.name)
		touch('%s/home/admin.py' % self.name)
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
		mkdir('static/templates/home')
		
	def setup_migrations(self):
		run('python manage.py makemigrations')
		run('python manage.py migrate')	

	
	def create_project(self):
		run('django-admin.py startproject %s' % self.name)
		
	def make_file(self,fdir,fname,fto_path,ctx=None):
		'''
			directory where file comes from
			files name
			where file gets printed
			context if any
		'''
		sfile = fcombine(fdir,fname,ctx)
		create_file(fto_path,sfile)

	def make_url_file(self):
		self.make_file(
			self.urls_dir['urls'],
			'urls.py',
			"%s%s" % (self.app_paths['urls'],'%s/urls.py' % self.name)
		)

	def make_settings_dir(self):
		self.make_file(
			self.settings_dir['settings'],
			'common.py',
			"%s%s" % (self.app_paths['settings'],'settings/common.py')
		)

		self.make_file(
			self.settings_dir['settings'],
			'local.py',
			"%s%s" % (self.app_paths['settings'],'settings/local.py')
		)

		self.make_file(
			self.settings_dir['settings'],
			'production.py',
			"%s%s" % (self.app_paths['settings'],'settings/production.py')
		)

	def install_requirements(self,key):
		with virtualenv('%s/bin' % self.name):
			run_install(self.reqire_dir[key])	

	def start_server(self):
		run('python manage.py runserver')

	def move_files_over(self):
		cpm(
			self.settings_dir['env'],
			"%s%s" % (self.app_paths['settings'],'%s/env.py' % self.name)
		)

		self.make_file(
			self.settings_dir['settings_dir'],
			'settings.py',
			"%s%s" % (self.app_paths['settings'],'%s/settings.py' % self.name),
			{'sitename' : self.name}
		)

		cpm(
			self.views_dir['home'],
			"%s%s" % (self.app_paths['root'],"%s/home/views.py" % self.name)
		)

		cpm(
			self.templates_dir['base'],
			"%s/%s" % (self.app_paths['app'],"static/templates/layouts/base.html")
		)

		cpm(
			self.templates_dir['home'],
			"%s/%s" % (self.app_paths['app'],"static/templates/home/index.html")
		)	

	def django_run_list(self,fn):
		scrub_project_name(self.name)
		cd(self.path)	
		self.make_virtual_env()
		self.install_requirements('development-test')	
		cd(self.name)
		self.create_project()
		fn()
		cd(self.app_paths['manage.py'])
		run('python manage.py makemigrations')
		run('python manage.py migrate')	
		run('python manage.py runserver')

class DjangoMonolith(Django):
	def __init__(self,name,path,type):
		Django.__init__(self,name,path,type)

	def monolith_run_list(self):
		self.make_static_dirs()
		self.make_static_files()
		self.make_url_file()
		self.move_files_over()

	def setup(self):
		self.django_run_list(self.monolith_run_list)

class DjangoApi(Django):
	def __init__(self,name,path,type):
		Django.__init__(self,name,path,type)

	def django_api_run_list(self):
		pass
		# self.make_static_dirs()
		# self.make_static_files()
		# self.make_url_file()
		# self.move_files_over()

	def setup(self):
		self.django_run_list(self.django_api_run_list)
		
		

