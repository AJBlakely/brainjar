from django.contrib import admin
from .models import Topic, Note, Tag

admin.site.register(Topic)
admin.site.register(Note)
admin.site.register(Tag)
