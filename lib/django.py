from lib.util import *
from lib.templates import t_gen

class Django(object):
	def __init__(self,name,path,type):
		self.name = name 
		self.path = path 
		self.type = type
		
		# generator cli path lookups
		self.gpath_lookup = {
			'settings' : {
				'settings_dir' : "%s/templates/django/settings" % get_rd(),
				'settings.py' : "%s/templates/django/settings/settings.py" % get_rd(),
				'env.py' : "%s/templates/django/settings/env.py" % get_rd()
			},
			'urls' : {
				'urls_dir' : "%s/templates/django/urls" % get_rd(),
				'urls.py' : "%s/templates/django/urls/urls.py" % get_rd(),
			},
			'templates' : {
				'home' : {
					'index.html' : "%s/templates/django/templates/home/index.html" % get_rd(),
				},
				'layouts' : {
					'base.html' : "%s/templates/django/templates/layouts/base.html" % get_rd()
				}
			},
			'views' : {
				'home' : {
					'views.py' : "%s/templates/django/views/home/views.py" % get_rd()
				}
			},
			'requirements' : {
				'development.txt' : "%s/templates/django/requirements/development.txt" % get_rd(),
				'development-test.txt' :  "%s/templates/django/requirements/development-test.txt" % get_rd()
			}
		}


		# django app directory lookup
		self.dpath_lookup = {
			'app' : "%s/%s" % (path,name),
			'venv' : path,
			'settings' : "%s/%s/%s/" % (path,name,name),
			'urls' : "%s/%s/%s/" % (path,name,name),
			'root' : "%s/%s/" % (path,name),
			'manage.py' : "%s/%s/%s" % (path,name,name),
		}

		self.dapp_lookup = {
			'settings' : {
				'production.py' : "%s%s" % (self.dpath_lookup['settings'],'settings/production.py'),
				'local.py' : "%s%s" % (self.dpath_lookup['settings'],'settings/local.py'),
				'common.py' : "%s%s" % (self.dpath_lookup['settings'],'settings/common.py'),
				'settings.py' : "%s%s" % (self.dpath_lookup['settings'],'%s/settings.py' % self.name),
				'env.py' : "%s%s" % (self.dpath_lookup['settings'],'%s/env.py' % self.name)
			},
			'urls' : {
				'urls.py' : "%s%s" % (self.dpath_lookup['urls'],'%s/urls.py' % self.name)
			},
			'templates' : {
				'home' : {
					'index.html' : "%s/%s" % (self.dpath_lookup['app'],"static/templates/home/index.html")
				},
				'layouts' : {
					'base.html' : "%s/%s" % (self.dpath_lookup['app'],"static/templates/layouts/base.html")
				}
			},
			'views' : {
				'home' : {
					'views.py' : "%s%s" % (self.dpath_lookup['root'],"%s/home/views.py" % self.name)
				}
			}
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
			self.gpath_lookup['urls']['urls_dir'],
			'urls.py',
			self.dapp_lookup['urls']['urls.py']
		)

	def make_settings_dir(self):
		self.make_file(
			self.gpath_lookup['settings']['settings_dir'],
			'common.py',
			self.dapp_lookup['settings']['common.py']
		)

		self.make_file(
			self.gpath_lookup['settings']['settings_dir'],
			'local.py',
			self.dapp_lookup['settings']['local.py']
		)

		self.make_file(
			self.gpath_lookup['settings']['settings_dir'],
			'production.py',
			self.dapp_lookup['settings']['production.py']
		)

	def install_requirements(self,key):
		with virtualenv('%s/bin' % self.name):
			run_install(self.gpath_lookup['requirements'][key])	

	def start_server(self):
		run('python manage.py runserver')

	def move_files_over(self):
		cpm(
			self.gpath_lookup['urls']['urls.py'],
			self.dapp_lookup['urls']['urls.py']
		)

		cpm(
			self.gpath_lookup['settings']['env.py'],
			self.dapp_lookup['settings']['env.py']
		)

		self.make_file(
			self.gpath_lookup['settings']['settings_dir'],
			'settings.py',
			self.dapp_lookup['settings']['settings.py'],
			{'sitename' : self.name}
		)

		cpm(
			self.gpath_lookup['views']['home']['views.py'],
			self.dapp_lookup['views']['home']['views.py']
		)

		cpm(
			self.gpath_lookup['templates']['layouts']['base.html'],
			self.dapp_lookup['templates']['layouts']['base.html']
		)

		cpm(
			self.gpath_lookup['templates']['home']['index.html'],
			self.dapp_lookup['templates']['home']['index.html']
		)	

	def django_run_list(self,fn):
		scrub_project_name(self.name)
		cd(self.path)	
		self.make_virtual_env()
		self.install_requirements('development-test.txt')	
		cd(self.name)
		self.create_project()
		fn()
		cd(self.dpath_lookup['manage.py'])
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
		
		

