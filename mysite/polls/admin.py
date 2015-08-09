from django.contrib import admin
from .models import Question, Choice

# Register your models here.
# 'was_published_recently is a function on the Quesiton Model class 
# TabularInline is a keyword, so is extra 
# https://docs.djangoproject.com/en/1.8/intro/tutorial02/
class ChoiceInline(admin.TabularInline):		#Much nicer then StackedInline
	model = Choice
	extra = 3 			
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['question_text']}), 
	('Date information', {'fields':['pub_date'],'classes':['collapse']}), ]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
