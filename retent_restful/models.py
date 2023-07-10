from django.db import models

class User(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    emailAddress = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=45)

class Deck(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    deckName = models.CharField(max_length=100, default='sample')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deckFavorite = models.BooleanField(default=False)
    averageAnswerTime = models.CharField(max_length=255, null=True)

class Card(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    answerCorrect = models.BooleanField(default=False)
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=400)
    interval = models.IntegerField()
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    answerTime = models.IntegerField(null=True)
    cardFavorite = models.BooleanField(default=False)

class Tag(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    tagName = models.CharField(max_length=40)
    tagColor = models.CharField(max_length=40, default='WHITE')

class TagToCard(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

class DeckHistory(models.Model):
    deckAnswerTime = models.IntegerField()
    createAt = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    accuracy = models.FloatField(default=0)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
