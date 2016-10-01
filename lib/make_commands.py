from lib.django import Django

def get_command(options):
	action = options['action-type']
	loaded_func = None
	if action == 'route':
		args = options['args']
		loaded_func = options['cmd']['type']['make']['route'](args)
	return loaded_func

def run(cmd):
	return cmd