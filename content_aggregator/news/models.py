import uuid

from django.db import models

from .choices import NEWS_CATEGORY

class TimeStampedUUID(models.Model):
	"""
	Abstract Model 
	"""

	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class News(TimeStampedUUID):

    category = models.CharField(max_length = 15, choices = NEWS_CATEGORY)
    title = models.CharField(
		max_length=255
	)
    link = models.URLField()
    description = models.TextField(blank=True, null=True)
    images_link = models.URLField()

    def __str__(self):
        return self.title