from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 		# overkill 
from django.template import RequestContext, loader 	#overkill 
from django.http import Http404				#overkill 
from .models import Question 

# https://docs.djangoproject.com/en/1.8/intro/tutorial03/
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')			# load a tempalte called ...
	#context is a dictionry mapping template variables to python objects 
	context = RequestContext(request, { 'latest_question_list':latest_question_list,})
	return HttpResponse(template.render(context))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	response = "You are looking atht eh results of question %s. "
	return HttpResponse(response % question_id)

def vote(request, question_id): 
	return HttpResponse("You are voting on question %s." % question_id)