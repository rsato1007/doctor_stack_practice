from django.db import models

# Create your models here.
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    # Documentation on class meta options: https://docs.djangoproject.com/en/3.2/ref/models/options/
    class Meta:
        ordering = ["created"]