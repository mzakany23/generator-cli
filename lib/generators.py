from lib.django import DjangoMonolith,DjangoApi

class Generators(DjangoMonolith):
	def __init__(self,type,name,path):
		
		self.type = type
		self.name = name 
		self.path = path
		self.command_lookup = {
			'django' : self.generate_django_monolith,
			'djangoapi' : self.generate_django_api
		}
	
	def generate_django_monolith(self):
		d = DjangoMonolith(self.name,self.path,self.type)
		d.setup()

	def generate_django_api(self):
		d = DjangoApi(self.name,self.path,self.type)
		d.setup()

	def generate_webpack_riot_app(self):
		pass

	def generate_django_api_webpack(self):
		pass

	def run(self):
		return self.command_lookup[self.type]()
		
    
	
