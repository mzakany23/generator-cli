from jinja2 import Environment, FileSystemLoader

def t_gen(path):
	j2_env = Environment(loader=FileSystemLoader(path),trim_blocks=True)	
	def inner(f,ctx=None):
		return j2_env.get_template(f).render(ctx) if ctx else j2_env.get_template(f).render()
	return inner