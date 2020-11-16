import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import utc

class Trinker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    motto = models.TextField()
    dabei = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Pruegel(models.Model):
    schlaeger = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING,related_name='schlaeger')
    geschlagen = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING,related_name='geschlagen')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "von " + self.schlaeger.user.username + " zu " + self.geschlagen.user.username

class Kuss(models.Model):
    kuesser = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING,related_name='kuesser')
    gekuesster = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING,related_name='gekuesster')
    antwort = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "von "+self.kuesser.user.username + " zu " + self.gekuesster.user.username

class Kneipe(models.Model):
    name = models.TextField()
    trinker = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING)
    reihenfolge = models.IntegerField()

class Steuerung(models.Model):
    kneipe = models.ForeignKey(Kneipe, on_delete=models.DO_NOTHING)
    reactionrunden = models.IntegerField()

class Bier(models.Model):
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE,related_name='biere')
    created_date = models.DateTimeField(default=timezone.now)

    def trinkzeit(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.created_date
        return timediff.total_seconds()/60

class ReactionChallenge(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    answered_at = models.DateTimeField()
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE)

class QuestionTemplate(models.Model):
    questiontext = models.TextField()
    answertext = models.TextField()

class QuestionRound(models.Model):
    template = models.ForeignKey(QuestionTemplate, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class QuestionAnswer(models.Model):
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE)
    questionround = models.ForeignKey(QuestionRound, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class Busfahrt(models.Model):
    created_date = models.DateTimeField(default=timezone.now)

class Bussitzer(models.Model):
    fahrt = models.ForeignKey(Busfahrt, on_delete=models.CASCADE)
    fahrer = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(default=timezone.now)

class Countdown(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    interval = models.IntegerField()

    def __str__(self):
        return str(self.created_date) + " with "+ str(self.interval)+" seconds"

class CountdownTeilnehmer(models.Model):
    countdown = models.ForeignKey(Countdown, on_delete=models.CASCADE)
    teilnehmer = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING)
    erfolg = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Countdown "+str(self.countdown.id)+ ": "+self.teilnehmer.user.username+". Erfolg:"+ str(self.erfolg)