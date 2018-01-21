from django.shortcuts import render
from django.db.models import Max, Min
from math import floor
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (Event, Entity, NewsSource, Article, NewsSourceEntityAssoc, ArticleEntityAssoc)


def index(request):
    """
    This is the index view.
    """

    events_dict = dict()
    events = Event.objects.all().order_by('-start_date')
    expand_rows = dict()
    # .annotate(max_sentiment=Max('articles_related__overall_sentiment'), min_sentiment=Min('articles_related__overall_sentiment'))

    # grab the articles for each event that had the max 
    for event in events:
        articles = event.articles_related.all().order_by('overall_sentiment')
        most_positive = articles[0]
        most_negative = articles[articles.count() - 1]
        # most_positive = event.articles_related.filter(sentiment=event.max_sentiment).order_by('-date')
        # most_negative = event.articles_related.filter(sentiment=event.min_sentiment).order_by('-date')
        events_dict[event.id] = [most_positive, most_negative]
        most_positive_id = most_positive.id
        most_negative_id = most_negative.id

        most_positive_article = Article.objects.get(id=most_positive_id)
        most_negative_article = Article.objects.get(id=most_negative_id)

        event = most_positive_article.event

        other_articles = Article.objects.filter(event=event).exclude(id__in=[most_positive_id, most_negative_id]).order_by('overall_sentiment')
        positive_articles = other_articles[0:int(floor(other_articles.count() / 2))]
        negative_articles = other_articles[int(floor(other_articles.count() / 2)): other_articles.count() - 1]
        expand_rows[event.id] = [positive_articles, negative_articles]

        # print("<-----------------------")
        # print(articles.count())

        # arts = Article.objects.filter(event=event)
        # print(arts.count())
        # print("<-----------------------")

    # numbers_list = range(1, 50)
    paginator = Paginator(events, 7)
      
    page = request.GET.get('page')
    numbers = paginator.get_page(page) #replace numbers_list and numbers with actual articles
    
    #Collect Articles
    # articles = Article.objects.all().order_by('-overall_sentiment')

    #Collect ArticleEntityAssocs
    # article_entity_assocs = ArticleEntityAssoc.objects.all().order_by('-sentiment')

    #Pair the articles with the most positive and negative sentiments

    # print(numbers)
    context = {
        'events_dict':events_dict,
        'other_articles':expand_rows,
        'numbers':numbers,
    }
    return render(request,"gotnews_app/index.html", context)

# def expand_row(request):
#     """
#     This will grab and return all data for row expansion.
#     """
#     most_positive_id = request.POST['most_positive_id']
#     most_negative_id = request.POST['most_negative_id']

#     most_positive_article = Article.objects.get(id=most_positive_id)
#     most_negative_article = Article.objects.get(id=most_negative_id)

#     event = most_positive_article.event

#     other_articles = Article.objects.filter(event=event).exclude(id__in=[most_positive_id, most_negative_id]).order_by('overall_sentiment')
#     positive_articles = other_articles[0:int(floor(other_articles.count() / 2))]
#     negative_articles = other_articles[int(floor(other_articles.count() / 2)): other_articles.count() - 1]
#     article_rows = [positive_articles, negative_articles]

#     context = {
#         'article_rows':article_rows
#     }

#     return render(request, 'gotnews_app/expand_row.html', context)

def entity_index(request):
    return HttpResponse("This will be the example entity index")
