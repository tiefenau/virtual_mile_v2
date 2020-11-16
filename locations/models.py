from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)

    def get_last_location(self):
        return self.location_set.last()

    def add_location(self, lat, long):
        return self.location_set.create(latitude=lat, longitude=long)

    def __str__(self):
        return self.username

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Lat: "+ str(self.latitude)+ " + Long:"+str(self.longitude)+ " on " + str(self.timestamp)
