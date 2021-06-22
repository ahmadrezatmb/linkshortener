from django.db import models

# Create your models here.

class urlsdatabase(models.Model):
    urlbeforecut = models.URLField()
    visited = models.IntegerField()
    urlaftercut  = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.urlbeforecut} to {self.urlaftercut}'