from django.db import models

class Books(models.Model):
    """Books model"""
    title = models.TextField()
    author = models.TextField()
    genre = models.TextField()
    description = models.TextField()
    isbn = models.BigIntegerField()
    image = models.TextField()
    published = models.DateTimeField()
    publisher = models.TextField()

    def __str__(self):
        return f"Author: {self.author} | title: {self.title}"
