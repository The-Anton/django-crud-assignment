from django.contrib import admin

from products.models import Box

admin.sites.site.register(Box)
