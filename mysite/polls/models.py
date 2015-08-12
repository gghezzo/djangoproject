from django.db import models			
import datetime 
from django.utils import timezone
# Note: My import is different then the guide https://docs.djangoproject.com/en/1.8/intro/tutorial05/

# This is a tutorial from https://docs.djangoproject.com/en/1.8/intro/tutorial01/
# I do not undersatnd the was_published_recently attributes. Methods? see list_display 
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __str__(self): 
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'		# huh
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently'


class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.choice_text
