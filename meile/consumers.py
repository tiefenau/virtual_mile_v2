# chat/consumers.py
import json
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Count

from .models import Trinker, Bier, Pruegel, Busfahrt, Bussitzer, Kuss, Countdown
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "trinker_room",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        #message = text_data_json['message']

        if(type == "hauen"):
            hit = text_data_json['opfer']
            hitter = text_data_json['hauer']
            hauer = User.objects.get(username=hitter)
            geschlagen = User.objects.get(username=hit)
            Pruegel.objects.create(schlaeger=hauer.trinker, geschlagen=geschlagen.trinker)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'hauen',
                    'hit': hit,
                    'hitter': hitter,
                    'newcount': geschlagen.trinker.geschlagen.count()
                }
            )
        elif (type=="trink"):
            trinkername = text_data_json['trinker']
            t = User.objects.get(username=trinkername)
            Bier.objects.create(trinker=t.trinker)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'trinken',
                    'trinker': trinkername,
                    'newcount': t.trinker.biere.count()
                }
            )
        elif (type=="updateall"):
            ts = Trinker.objects.all()
            ts_o = []
            for t in ts:
                letztes_bier = t.biere.last()
                kisses = t.gekuesster.count() + t.kuesser.count()
                kisses_success = t.gekuesster.filter(antwort=1).count()+t.kuesser.filter(antwort=1).count()
                ts_o.append({
                    'name': t.user.username,
                    'lastbeer': letztes_bier.trinkzeit() if letztes_bier else -1,
                    'kisses': kisses,
                    'kisses_success':kisses_success
                })
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'update',
                    't': ts_o
                }
            )
        elif (type=="busstart"):
            fahrt = Busfahrt.objects.create()
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'busstart',
                    'fahrt_id': fahrt.id
                }
            )
        elif (type=="einsteigen"):
            fahrt_id = text_data_json['fahrt_id']
            trinkername = text_data_json['fahrer']
            t = User.objects.get(username=trinkername)
            fahrt = Busfahrt.objects.get(id=fahrt_id)
            Bussitzer.objects.create(fahrt = fahrt, fahrer = t.trinker)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'einstieg',
                    'trinker': trinkername
                }
            )
        elif (type=="losfahren"):
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'losfahren',
                }
            )
        elif (type == "noten"):
            trinkername = text_data_json['trinker']
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'message',
                    'message': trinkername + ": "+message
                }
            )
        elif (type == "kiss"):
            von = text_data_json['von']
            zu = text_data_json['zu']
            kuesser = User.objects.get(username=von)
            if zu == "random":
                gekuesster = random.choice(User.objects.all())
            else:
                gekuesster = User.objects.get(username=zu)
            k = Kuss.objects.create(kuesser=kuesser.trinker, gekuesster=gekuesster.trinker, antwort=-1)
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'kiss',
                    'von': von,
                    'zu': gekuesster.username,
                    'brokiss_id': k.id
                }
            )
        elif (type=="kissanswer"):
            brokiss_id = text_data_json['brokiss_id']
            k = Kuss.objects.get(id=brokiss_id)
            k.antwort = text_data_json['antwort']
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'kissanswer',
                    'kuss_id': k.id,
                    'von': k.kuesser.user.username,
                    'zu': k.gekuesster.user.username,
                    'antwort': k.antwort
                }
            )
        elif (type=="saufalarm"):
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'saufalarm',
                    'time': 100 if text_data_json['method'] == 'immediately' else random.randint(1000,300000)
                }
            )
        elif (type=="saufcountdown"):
            c = Countdown.objects.create(interval = text_data_json['interval'])
            async_to_sync(self.channel_layer.group_send)(
                "trinker_room",
                {
                    'type': 'saufcountdown',
                    'time': text_data_json['interval'],
                    'countdown_id': c.id
                }
            )
        elif (type=="donecountdown"):
            c = Countdown.objects.get(id=text_data_json['countdown_id'])
            u = User.objects.get(username=text_data_json['user'])
            c.countdownteilnehmer_set.create(teilnehmer=u.trinker, erfolg=text_data_json['erfolg'])
            c.save()

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))

    def update(self, event):
        self.send(text_data=json.dumps({
            'type': 'update',
            'trinker': event['t']
        }))

    def trinken(self, event):
        trinker = event['trinker']
        newcount = event['newcount']
        self.send(text_data=json.dumps({
            'type': 'trink',
            'trinker': trinker,
            'newcount': newcount
        }))

    def hauen(self, event):
        hit = event['hit']
        hitter = event['hitter']
        newcount = event['newcount']
        self.send(text_data=json.dumps({
            'type': 'hauen',
            'hit': hit,
            'hitter': hitter,
            'newcount': newcount
        }))

    def kiss(self, event):
        von = event['von']
        zu = event['zu']
        self.send(text_data=json.dumps({
            'type': 'brokissrein',
            'von': von,
            'zu': zu,
            'brokiss_id': event['brokiss_id']
        }))

    def kissanswer(self, event):
        self.send(text_data=json.dumps({
            'type': 'kissanswer',
            'antwort': event['antwort'],
            'von': event['von'],
            'zu': event['zu'],
            'brokiss_id': event['kuss_id']
        }))

    def busstart(self, event):
        self.send(text_data=json.dumps({
            'type': 'busstart',
            'fahrt_id': event['fahrt_id']
        }))

    def einstieg(self, event):
        trinker = event['trinker']
        self.send(text_data=json.dumps({
            'type': 'einstieg',
            'trinker': trinker,
        }))

    def losfahren(self, event):
        self.send(text_data=json.dumps({
            'type': 'losfahren',
        }))

    def saufalarm(self, event):
        self.send(text_data=json.dumps({
            'type': 'saufalarm',
            'time': event['time']
        }))

    def saufcountdown(self, event):
        self.send(text_data=json.dumps({
            'type': 'saufcountdown',
            'time': event['time'],
            'countdown_id': event['countdown_id']
        }))

    def message(self, event):
        self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message']
        }))