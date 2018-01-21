# usr/bin/python3
from google.cloud import language

def main():
	# intialize google-cloud language client
	client = language.LanguageServiceClient()

	friends = ["Sally", "Alex", "Donald", "Haley", "Alec", 
				"Adrien", "Cynthia", "Jakob", "Kira", 
				"Bradley", "Srujan", "Radhika", "Shonit", "Anuka"
	]

	actions = ["smiling", "laughing", "coding", "writing", 
		"playing Mass Effect", "reading Spiderman comics", 
		"watching Donnie Darko and then Citizen Kane"
	]
	# read in the match data
	practice_matrix_data = [i for i in range(0,100)]
	practice_article_data = [
		friends[i%len(friends)] + " " + actions[i%len(actions)]
		for i in range(0,100)
	]

	# create documents out of each article
	for i in practice_matrix_data:
		print(practice_article_data[i])
		# Create Django Article bbject
		document = language.types.Document(
			content=practice_article_data[i],
			language='en',
			type='PLAIN_TEXT'
		)

		# Get entities
		response = client.analyze_entities(document=document,  encoding_type='UTF32')

		# for entity in response.entities: 
		# 	# create Django Entity object
		# 	print("<--------------" + entity.name + "------------------>")

		# Get sentimental
		# Assign Article's overall sentiment
		response = client.analyze_sentiment(document=document,  encoding_type='UTF32')
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + str(response.document_sentiment) + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


		# get sentimental entities
		response = client.analyze_entity_sentiment(document=document,  encoding_type='UTF32')
		for entity in response.entities:
			# Get-Or-Create Django Entity, ArticleEntityAssoc & set sentiment
			# Do some averaging for the NewsSourceEntityAssoc sentiment value
			print("###################### " + entity.name + " sentiment:" + str(entity.sentiment.magnitude) + " ###################")




main()