from django.db import models



class UrlModels(models.Model):
    url_before_cut = models.URLField()
    visited = models.IntegerField()
    url_after_cut  = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.url_before_cut} to {self.url_after_cut}'