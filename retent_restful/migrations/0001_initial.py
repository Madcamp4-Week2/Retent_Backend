# Generated by Django 4.2.3 on 2023-07-10 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('answerCorrect', models.BooleanField(default=False)),
                ('question', models.CharField(max_length=300)),
                ('answer', models.CharField(max_length=400)),
                ('interval', models.IntegerField()),
                ('answerTime', models.IntegerField(null=True)),
                ('cardFavorite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('deckName', models.CharField(default='sample', max_length=100)),
                ('deckFavorite', models.BooleanField(default=False)),
                ('averageAnswerTime', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('tagName', models.CharField(max_length=40)),
                ('tagColor', models.CharField(default='WHITE', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('emailAddress', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='TagToCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retent_restful.card')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retent_restful.tag')),
            ],
        ),
        migrations.CreateModel(
            name='DeckHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deckAnswerTime', models.IntegerField()),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('accuracy', models.FloatField(default=0)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retent_restful.deck')),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retent_restful.user'),
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retent_restful.deck'),
        ),
    ]
