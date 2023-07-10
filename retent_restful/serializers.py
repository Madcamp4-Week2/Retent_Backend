from rest_framework import serializers
from .models import User, Deck, Card, Tag, TagToCard,DeckHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',  'emailAddress', 'password', 'nickname')

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ('id','deckName','user','deckFavorite')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id','answerCorrect','question','answer','interval','deck','answerTime','cardFavorite')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','tagName','tagColor')

class TagToCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagToCard
        fields = ('deck','tag')

class DeckHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckHistory
        fields = ('deckAnswerTime','accuracy','deck')
