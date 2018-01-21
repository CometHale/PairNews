# usr/bin/python3
from datetime import datetime
from random import randint
from django.utils.timezone import make_aware, get_default_timezone
from ..models import (Event, Entity, NewsSource, Article, NewsSourceEntityAssoc, ArticleEntityAssoc)

def main():

	for i in range(0,11): # generate 10 Events
		name = "x" * i
		start_date = make_aware(datetime(1, 1 + i, 2018), get_default_timezone())
		end_date = make_aware(datetime(1, 1 + randint(1,15) , 2018), get_default_timezone())
		event = Event.objects.create(name=name, start_date=start_date, end_date=end_date)

	persons = ["Sally", "Alex", "Donald", "Haley", "Alec", 
				"Adrien", "Cynthia", "Jakob", "Kira", 
				"Bradley", "Srujan", "Radhika", "Shonit", "Anuka"]
	
	for person in persons:
		entity = Entity.objects.create(name=person)

	newses = ["CNN", "Breitbart", "The Washington Post", "Fox", "The Onion", "The Root", "BBC", "Aljazeera"]

	for news in newses



main()