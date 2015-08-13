from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse 
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic 
from django.utils import timezone 

from .models import Question 
from django.template import RequestContext, loader 	#overkill 
# from django.http import Http404				#overkill 

# https://docs.djangoproject.com/en/1.8/intro/tutorial03/
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		""" Return the last 5 published questions """
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

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