from lib.django import DjangoMonolith

class Generators(DjangoMonolith):
	def __init__(self,type,name,path):
		
		self.type = type
		self.name = name 
		self.path = path
		self.command_lookup = {
			'django' : self.generate_django_monolith
		}
	
	
	def generate_django_monolith(self):
		d = DjangoMonolith(self.name,self.path,self.type)
		d.setup()

		pass

	def generate_django_api(self):
		pass

	def generate_webpack_riot(self):
		pass

	def generate_django_api_webpack(self):
		pass

	def run(self):
		return self.command_lookup[self.type]()
		
    
	
