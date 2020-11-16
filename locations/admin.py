from django.contrib import admin

# Register your models here.
from locations.models import User, Location

admin.site.register(User)
admin.site.register(Location)