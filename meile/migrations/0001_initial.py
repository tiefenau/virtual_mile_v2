# Generated by Django 3.1.3 on 2020-11-14 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Busfahrt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Kneipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('reihenfolge', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questiontext', models.TextField()),
                ('answertext', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Trinker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Steuerung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reactionrunden', models.IntegerField()),
                ('kneipe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='meile.kneipe')),
            ],
        ),
        migrations.CreateModel(
            name='ReactionChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('answered_at', models.DateTimeField()),
                ('trinker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meile.trinker')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meile.questiontemplate')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('questionround', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meile.questionround')),
                ('trinker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meile.trinker')),
            ],
        ),
        migrations.CreateModel(
            name='Pruegel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('geschlagen', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='geschlagen', to='meile.trinker')),
                ('schlaeger', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='schlaeger', to='meile.trinker')),
            ],
        ),
        migrations.AddField(
            model_name='kneipe',
            name='trinker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='meile.trinker'),
        ),
        migrations.CreateModel(
            name='Bussitzer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('fahrer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='meile.trinker')),
                ('fahrt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meile.busfahrt')),
            ],
        ),
        migrations.CreateModel(
            name='Bier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('trinker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biere', to='meile.trinker')),
            ],
        ),
    ]
