# usr/bin/python3
from google.cloud import language
import json
from datetime import datetime
from decimal import Decimal
from similarity.ParseMatrix import get_topics_list 
from gotnews_app.models import (Event, Entity, Article, NewsSource, NewsSourceEntityAssoc, ArticleEntityAssoc)

def main():
	# intialize google-cloud language client
	client = language.LanguageServiceClient()

	# read in the match data
	with open('./data_processing/scrape_store.json') as file:
		textArr = json.load(file)
		topicsList = get_topics_list(textArr)

	# create documents out of each article
	for lst in topicsList:

		event, created = Event.objects.get_or_create(name=lst[0]['title']) #create the 
		if created:
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~ NEW TOPIC:" + lst[0]['title'] + " ~~~~~~~~~~~~~~~~~~~~~~~~~~" )
		
		for article in lst:

			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEW ARTICLE !!!!!!!!!!!!!!!!!!!!!!!!!!")
			document = language.types.Document(
				content=article['textData'],
				language='en',
				type='PLAIN_TEXT'
			)
			# create Django Event object
			
			# Get sentimental
			# Assign Article's overall sentiment
			response = client.analyze_sentiment(document=document,  encoding_type='UTF32')
			# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + str(response.document_sentiment) + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

			# Create Django Article object
			date = datetime.strptime(article['publishDate'][0:9], '%Y-%m-%d')
			response = client.analyze_sentiment(document=document,  encoding_type='UTF32')
			overall_sentiment = response.document_sentiment.magnitude * response.document_sentiment.score

			news_source, created = NewsSource.objects.get_or_create(name=article['sourceName'])
			title = article['title']
			url = article['url']
			article, created = Article.objects.get_or_create(date=date, overall_sentiment=overall_sentiment, title=title, url=url, news_source=news_source, event=event)

			# get sentimental entities
			response = client.analyze_entity_sentiment(document=document,  encoding_type='UTF32')
			for entity in response.entities:
				# Get-Or-Create Django Entity, ArticleEntityAssoc & set sentiment
				new_entity, created = Entity.objects.get_or_create(name=entity.name)
				if created:
					print("<--------------" + entity.name + " ------------------>")

				news_assoc, created = NewsSourceEntityAssoc.objects.get_or_create(news_source=news_source, entity=new_entity)
				article_assoc, created = ArticleEntityAssoc.objects.get_or_create(article=article, entity=new_entity)
				
				article_count = ArticleEntityAssoc.objects.filter(entity=new_entity).count()
				news_article_count = NewsSourceEntityAssoc.objects.filter(entity=new_entity, news_source=news_source).count()
				if not created:
					old_news_sentiment = news_assoc.sentiment * (news_article_count - 1)
					new_news_sentiment = old_news_sentiment + Decimal(entity.sentiment.magnitude * entity.sentiment.score)
					news_assoc.sentiment = new_news_sentiment / news_article_count
					
					old_article_sentiment = article_assoc.sentiment * (article_count - 1)
					new_article_sentiment = old_article_sentiment + Decimal(entity.sentiment.magnitude * entity.sentiment.score)
					article_assoc.sentiment = new_article_sentiment / article_count
					news_assoc.save()
					article_assoc.save()




main()