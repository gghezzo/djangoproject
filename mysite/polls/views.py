from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse 
from django.http import HttpResponse, HttpResponseRedirect

from .models import Question 
from django.template import RequestContext, loader 	#overkill 
# from django.http import Http404				#overkill 


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
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id): 
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', { 
			'question': p, 
			'error_message': "Please select a choice",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))