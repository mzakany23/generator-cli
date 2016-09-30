from lib import util

class Django(object):
	def __init__(self,name,path,type):
		self.name = name 
		self.path = path 
		self.type = type
		
		# generator cli path lookups
		self.gpath_lookup = {
			'settings' : {
				'settings_dir' : "%s/templates/django/settings" % util.get_rd(),
				'settings.py' : "%s/templates/django/settings/settings.py" % util.get_rd(),
				'env.py' : "%s/templates/django/settings/env.py" % util.get_rd()
			},
			'urls' : {
				'urls_dir' : "%s/templates/django/urls" % util.get_rd(),
				'urls.py' : "%s/templates/django/urls/urls.py" % util.get_rd(),
			},
			'templates' : {
				'home' : {
					'index.html' : "%s/templates/django/templates/home/index.html" % util.get_rd(),
				},
				'layouts' : {
					'base.html' : "%s/templates/django/templates/layouts/base.html" % util.get_rd()
				}
			},
			'views' : {
				'home' : {
					'views.py' : "%s/templates/django/views/home/views.py" % util.get_rd()
				}
			},
			'requirements' : {
				'development.txt' : "%s/templates/django/requirements/development.txt" % util.get_rd(),
				'development-test.txt' :  "%s/templates/django/requirements/development-test.txt" % util.get_rd()
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
		util.run('virtualenv %s' % self.name)

	def setup(self):
		raise NotImplementedError('You must implement the setup() method yourself!')

	def make_static_files(self):
		util.touch('.gitignore')
		util.touch('%s/home/__init__.py' % self.name)
		util.touch('%s/home/admin.py' % self.name)
		util.touch('%s/api/__init__.py' % self.name)

	def make_static_dirs(self):
		util.mkdir('docs')
		util.mkdir('logs')
		util.mkdir('tests')
		util.mkdir('static/static/assets/')
		util.mkdir('static/static/assets/js')
		util.mkdir('static/static/assets/css')
		util.mkdir('static/static/assets/img')
		util.mkdir('static/media')
		util.mkdir('static/root')
		util.mkdir('static/templates/layouts/partials')
		util.mkdir('static/templates/home')
		
	def setup_migrations(self):
		util.run('python manage.py makemigrations')
		util.run('python manage.py migrate')	

	
	def create_project(self):
		util.run('django-admin.py startproject %s' % self.name)
		
	def make_file(self,fdir,fname,fto_path,ctx=None):
		'''
			directory where file comes from
			files name
			where file gets printed
			context if any
		'''
		sfile = util.fcombine(fdir,fname,ctx)
		util.create_file(fto_path,sfile)

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

	def install_requirements(self,filename):
		with util.virtualenv('%s/bin' % self.name):
			util.run_install(self.gpath_lookup['requirements'][filename])	

	def start_server(self):
		util.run('python manage.py runserver')

	def move_files_over(self):
		util.cpm(
			self.gpath_lookup['urls']['urls.py'],
			self.dapp_lookup['urls']['urls.py']
		)

		util.cpm(
			self.gpath_lookup['settings']['env.py'],
			self.dapp_lookup['settings']['env.py']
		)

		self.make_file(
			self.gpath_lookup['settings']['settings_dir'],
			'settings.py',
			self.dapp_lookup['settings']['settings.py'],
			{'sitename' : self.name}
		)

		util.cpm(
			self.gpath_lookup['views']['home']['views.py'],
			self.dapp_lookup['views']['home']['views.py']
		)

		util.cpm(
			self.gpath_lookup['templates']['layouts']['base.html'],
			self.dapp_lookup['templates']['layouts']['base.html']
		)

		util.cpm(
			self.gpath_lookup['templates']['home']['index.html'],
			self.dapp_lookup['templates']['home']['index.html']
		)	

	def django_run_list(self,fn):
		util.scrub_project_name(self.name)
		util.cd(self.path)	
		self.make_virtual_env()
		self.install_requirements('development-test.txt')	
		util.cd(self.name)
		self.create_project()
		fn()
		util.cd(self.dpath_lookup['manage.py'])
		util.run('python manage.py makemigrations')
		util.run('python manage.py migrate')	
		util.run('python manage.py runserver')

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
		
		

