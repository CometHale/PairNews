from django.shortcuts import render
from django.db.models import Max, Min
from django.http import HttpResponse
from .models import (Event, Entity, NewsSource, Article, NewsSourceEntityAssoc, ArticleEntityAssoc)


def index(request):
	"""
	This is the index view.
	"""

	events_dict = dict()
	events = Event.objects.all().order_by('-start_date')
	# .annotate(max_sentiment=Max('articles_related__overall_sentiment'), min_sentiment=Min('articles_related__overall_sentiment'))

	# grab the articles for each event that had the max 
	for event in events:
		articles = event.articles_related.all().order_by('overall_sentiment')
		most_positive = articles[0]
		most_negative = articles[articles.count() - 1]
		# most_positive = event.articles_related.filter(sentiment=event.max_sentiment).order_by('-date')
		# most_negative = event.articles_related.filter(sentiment=event.min_sentiment).order_by('-date')
		# events_dict[event.id] = [most_positive, most_negative]

  numbers_list = range(1, 50)
  paginator = Paginator(numbers_list, 7)
  
  page = request.GET.get('page')
  numbers = paginator.get_page(page) #replace numbers_list and numbers with actual articles
	
	#Collect Articles
	# articles = Article.objects.all().order_by('-overall_sentiment')

	#Collect ArticleEntityAssocs
	# article_entity_assocs = ArticleEntityAssoc.objects.all().order_by('-sentiment')

	#Pair the articles with the most positive and negative sentiments

	context = {}
	return render(request,"gotnews_app/index.html", {'numbers':numbers,  'context': context})

def expand_row(request):
	"""
	This will grab and return all data for row expansion.
	"""
	# will need the id of the article in question
	return HttpResponse("This will return the data to expand a row with.")
