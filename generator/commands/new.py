"""The generate command."""

from json import dumps

from .base import Base

from lib.generators import Generators

class Generate(Base):
	"""Generate Projects"""
	
	def generate_project(self,type,name,path):
		g = Generators(type,name,path)
		g.run()

	def run(self):
		self.generate_project(self.project,self.name,self.path)		
		
    	
        
