# usr/bin/python3
from google.cloud import language
import json
from similarity.ParseMatrix import get_topics_list 
# from gotnews_app.models import (Event, Entity, Article, NewsSource, NewsSourceEntityAssoc, ArticleEntityAssoc)

def main():
	# intialize google-cloud language client
	client = language.LanguageServiceClient()

	# read in the match data
	with open('./data_processing/scrape_store.json') as file:
		textArr = json.load(file)
		topicsList = get_topics_list(textArr)

	# create documents out of each article
	for lst in topicsList:
		for article in lst:

			print("!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEW ARTICLE !!!!!!!!!!!!!!!!!!!!!!!!!!")
			document = language.types.Document(
				content=article['textData'],
				language='en',
				type='PLAIN_TEXT'
			)
			# create Django Event object
			# event = Event.objects.create()

			# Create Django Article object
			# article = Article.objects.create()

			# Get entities
			response = client.analyze_entities(document=document,  encoding_type='UTF32')
			
			# for entity in response.entities: 
			# 	# create Django Entity object
			# 	print("<--------------" + entity.name + "------------------>")

			# Get sentimental
			# Assign Article's overall sentiment
			response = client.analyze_sentiment(document=document,  encoding_type='UTF32')
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + str(response.document_sentiment) + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			# article.sentiment = response.document_sentiment.magnitude
			# article.save()

			# get sentimental entities
			response = client.analyze_entity_sentiment(document=document,  encoding_type='UTF32')
			for entity in response.entities:
				# Get-Or-Create Django Entity, ArticleEntityAssoc & set sentiment
				# entity = Entity.objects.get_or_create()
				# Do some averaging for the NewsSourceEntityAssoc sentiment value
				print("###################### " + entity.name + " sentiment:" + str(entity.sentiment.magnitude) + " ###################")




main()