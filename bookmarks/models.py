from django.db import models

# Create your models here.

class Bookmark(models.Model):

    title = models.CharField(max_length=100)
    url = models.URLField(max_length=300)
    tags = models.CharField(max_length=600)
    domain = models.CharField(default='', max_length=300)
    content = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    isCommitted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']


    def __str__(self):
        return ','.join([self.title,self.url])

