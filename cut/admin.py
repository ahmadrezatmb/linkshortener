from cut.models import urlsdatabase
from django.contrib import admin
from .models import urlsdatabase
# Register your models here.

class urlsregister(admin.ModelAdmin):
    pass

admin.site.register(urlsdatabase , urlsregister)
