from django.shortcuts import render
from django.http import HttpResponse
from .models import (Event, Entity, NewsSource, Article, NewsSourceEntityAssoc, ArticleEntityAssoc)


def index(request):
	"""
	This is the index view.
	"""
	#Collect Articles

	#Collect ArticleEntityAssocs

	#Pair the articles with the most positive and negative sentiments

	context = {}
	return render(request,template_name="gotnews_app/index.html", context=context)

def expand_row(request):
	"""
	This will grab and return all data for row expansion.
	"""
	# will need the id of the article in question
	return HttpResponse("This will return the data to expand a row with.")
