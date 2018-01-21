from django.test import TestCase
from .models import (Event, Entity, NewsSource, Article, NewsSourceEntityAssoc, ArticleEntityAssoc)

# Create your tests here.
class ExpandTestCase(TestCase):
	def setUp(self):
		

	def test_articles_same_topic(self):
		"""
		Tests whether or not the articles grabbed for row expansion
		correctly matched the topic of the article that was clicked for
		expansion.
		"""

		return self.assertEqual(1,1)