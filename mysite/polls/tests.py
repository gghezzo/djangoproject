from django.test import TestCase			# This was prepopulated
import datetime
from django.utils import timezone
from .models import Question
from django.core.urlresolvers import reverse 
# This was autocreated. Pretty cool 

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days) 
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionMethodTests(TestCase):
	# entries with time machiens are not recent 
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)

	# Grammy entries, even made today, are not recent  
	def test_was_published_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)

	# Baby entries, 1 hour old, are recent. Happy Case! 
	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

class QuestionViewTests(TestCase):
	# If no question exists, an appropriate msessage should be displayed
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
	# Question with past pub_date should be on index page
	
	def test_index_view_with_a_past_question(self):
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual( response.context['latest_question_list'], ['<Question: Past question.>'])

	def test_index_view_with_a_future_question(self):
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.", status_code=200)

	def test_index_view_with_future_question_and_past_question(self):
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual( response.context['latest_question_list'], ['<Question: Past question.>'])

	def test_index_view_with_two_past_questions(self):
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])


