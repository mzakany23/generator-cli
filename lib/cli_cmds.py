'''this file holds helper methods that parse cli commands'''

def make_route(*args):	
	args = args[0]
	return {
		'name' : "{0}.views as {0}_views".format(args[0]),
 		'url' : "url(r'^/{1}/$', {1}_views.create,name='{1}'),".format(args[0],args[1])
	}
	

def command_lookup(cmd):
	cl = {
		'action-type' : None,
		'project-type' : None,
		'site-name' : None,
		'path' : None,
		'cmd' : {
			'type' : {
				'new' : False,
				'make' : {
					'route' : make_route,
				}
			},				
		}
	}

	try:
		# generator new django:mysite
		if cmd['<cmd>']:
			cl['cmd']['type']['new'] = True
			cl['path'] = cmd['<path>'] if cmd['-p'] else False
			pn =  cmd['<project>:<name>'].split(':')
			ptype = pn[0]
			name = pn[1]
			cl['site-name'] = name 
			cl['project-type'] = ptype
	except:
		cl = False

	try:
		# generator make:django route products:create
		if cmd['<sub-cmd>:<project>']:
			sc = cmd['<sub-cmd>:<project>'].split(':')
			if sc[0] == 'make':
				cl['project-type'] = sc[1]
				cl['action-type'] = cmd['<type>']
				ca = cmd['<controller>:<action>'].split(':')
				cl['args'] = ca
				cl['cmd']['type']['make']['route']
	except:
		cl = False
	
	return cl












	