from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Trinker)
admin.site.register(Kneipe)
admin.site.register(Steuerung)
admin.site.register(ReactionChallenge)
admin.site.register(QuestionTemplate)
admin.site.register(QuestionRound)
admin.site.register(QuestionAnswer)
admin.site.register(Bier)
admin.site.register(Kuss)
admin.site.register(Pruegel)
admin.site.register(Countdown)
admin.site.register(CountdownTeilnehmer)