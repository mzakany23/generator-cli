from jinja2 import Environment, FileSystemLoader

def t_gen(path):
	j2_env = Environment(loader=FileSystemLoader(path),trim_blocks=True)	
	def inner(f,ctx):
		return j2_env.get_template(f).render(ctx)
	return inner