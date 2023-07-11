from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password, nickname, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not nickname:
            raise ValueError('Users must have a nickname')

        user = self.model(
            emailAddress=email,
            nickname=nickname,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    emailAddress = models.EmailField(unique=True)
    nickname = models.CharField(max_length=45)
    kakao_id = models.CharField(max_length=255, unique=True, null=True)  # 추가된 부분

    objects = UserManager()

    USERNAME_FIELD = 'emailAddress'
    REQUIRED_FIELDS = ['nickname']



class Deck(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    deckName = models.CharField(max_length=100, default='sample')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deckFavorite = models.BooleanField(default=False)

class Card(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    answerCorrect = models.BooleanField(default=False)
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=400)
    interval = models.IntegerField(null=True)
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
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,related_name='tag_cards')

class DeckHistory(models.Model):
    deckAnswerTime = models.IntegerField()
    createAt = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    accuracy = models.FloatField(default=0)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

