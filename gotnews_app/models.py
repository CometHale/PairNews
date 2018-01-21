from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

class Event(models.Model):
	name = models.CharField(max_length=1000)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	class Meta:
		verbose_name = 'EVENT'
		verbose_name_plural = 'EVENTS'

class Entity(models.Model):
	name = models.CharField(max_length=1000)
	occurrence_count = models.IntegerField(default=0)

	class Meta:
		verbose_name='ENTITY'
		verbose_name_plural='ENTITIES'

class NewsSource(models.Model):
	name = models.CharField(max_length=1000)

	class Meta:
		verbose_name='NEWSSOURCE'
		verbose_name_plural='NEWSSOURCES'

class Article(models.Model):
	date = models.DateField(null=True, blank=True)
	overall_sentiment = models.DecimalField(decimal_places=3, max_digits=5)
	title = models.CharField(max_length=1000)
	url = models.URLField(max_length=1000) # see if there is a url field
	event = models.ForeignKey(Event, related_name='articles_related', on_delete=models.CASCADE)
	news_source = models.ForeignKey(NewsSource, related_name='articles_related', on_delete=models.CASCADE)

	class Meta:
		verbose_name='ARTICLE'
		verbose_name_plural='ARTICLES'

class NewsSourceEntityAssoc(models.Model):
	news_source = models.ForeignKey(NewsSource, related_name='entities_related', on_delete=models.CASCADE)
	entity = models.ForeignKey(Entity, related_name='news_sources_related', on_delete=models.CASCADE)
	sentiment = models.DecimalField(decimal_places=3, max_digits=5)

	@receiver(post_save, dispatch_uid='<news_source_entity_id>')
	def increment_entity_occurence_count(sender, instance, created, raw, using, update_fields, **kwargs):
		if type(instance) == NewsSourceEntityAssoc:
			if created:
				instance.entity.occurrence_count += 1
				instance.entity.save()

	@receiver(pre_delete, dispatch_uid='<news_source_entity_id>')
	def decrement_entity_occurrence_count(sender, instance, using, **kwargs):
		if type(instance) == NewsSourceEntityAssoc:
			instance.entity.occurrence_count = instance.entity.occurrence_count - 1
			instance.entity.save()

	class Meta:
		verbose_name='NEWSSOURCEENTITYASSOC'
		verbose_name_plural='NEWSSOURCEENTITYASSOCS'

class ArticleEntityAssoc(models.Model):
	article = models.ForeignKey(Article, related_name='entities_related', on_delete=models.CASCADE)
	entity = models.ForeignKey(Entity, related_name='articles_related', on_delete=models.CASCADE)
	sentiment = models.DecimalField(decimal_places=3, max_digits=5)

	@receiver(post_save, dispatch_uid='<article_entity_id>')
	def increment_entity_occurence_count(sender, instance, created, raw,using, update_fields, **kwargs):
		if type(instance) == ArticleEntityAssoc:
			if created:
				instance.entity.occurrence_count += 1
				instance.entity.save()

	@receiver(pre_delete, dispatch_uid='<article_entity_id>')
	def decrement_entity_occurrence_count(sender, instance, using, **kwargs):
		if type(instance) == ArticleEntityAssoc:
			instance.entity.occurrence_count = instance.entity.occurrence_count - 1
			instance.entity.save()
	class Meta:
		verbose_name='ARTICLEENTITYASSOC'
		verbose_name_plural = 'ARTICLEENTITYASSOCS'
