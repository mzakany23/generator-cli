from django.core.urlresolvers import reverse
from django.shortcuts import render

def home(request):
	return render(request,'home/index.html',{})
