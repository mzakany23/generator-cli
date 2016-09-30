
def cli():

	lookup = {
		'make' : {
			'django' : {
				'routes' : {
					'create' : make_route
				}
			}
		}
	}


	def make_route(controller,action,path=None):
			return {
				'name' : "{0}.views as {0}_views".format(controller),
		 		'url' : "url(r'^/{0}$', {0}_views.create,name='{1}'),".format(action,controller)
			}

