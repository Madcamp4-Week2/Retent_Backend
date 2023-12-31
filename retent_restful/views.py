from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import User, Deck, Card, Tag, TagToCard,DeckHistory
from .serializers import UserSerializer, DeckSerializer, CardSerializer, TagSerializer, TagToCardSerializer,DeckHistorySerializer
import openai
import fitz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import action
from .secret_key import OPENAI_SECRET_KEY
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
import requests
from rest_framework_simplejwt.tokens import RefreshToken


openai.api_key =  OPENAI_SECRET_KEY

def get_user_id_from_token(request):
    authorization = request.headers.get('Authorization')
    if authorization is None:
        return None
    token = authorization.split(' ')[1]
    try:
        untyped_token = UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        raise InvalidToken('Given token not valid')

    user_id = untyped_token['user_id']
    return user_id


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = get_user_id_from_token(self.request)
        return User.objects.filter(id=user_id, status=1)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 0  
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(status=1)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 0  
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'], url_path='user_decks/(?P<userId>\d+)')
    def user_decks(self, request, userId=None):
        queryset = Deck.objects.filter(user_id=userId)
        serializer = DeckSerializer(queryset, many=True)
        return Response(serializer.data)
        

class DeckHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = DeckHistorySerializer

    def get_queryset(self):
        return User.objects.filter(status=1)
    
    @action(detail=False, methods=['POST'])
    def save_history(self, request, deckId=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(deck_id=deckId)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 0  
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        # Return "405 Method Not Allowed"
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['get'],url_path='recently')
    def latest_history(self, request):
        latest_deck_history = DeckHistory.objects.latest('createdAt')
        serializer = self.get_serializer(latest_deck_history)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.filter(status=1)

    @action(detail=False, methods=['GET'], url_path='deck_cards/(?P<deck_id>\d+)')
    def deck_cards(self, request, deck_id=None):
        queryset = Card.objects.filter(cardListId=deck_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 0  
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(status=1)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 0  
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagToCardViewSet(viewsets.ModelViewSet):
    queryset = TagToCard.objects.all()
    serializer_class = TagToCardSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 0  
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        # Return "405 Method Not Allowed"
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def retrieve(self, request, *args, **kwargs):
        # Return "405 Method Not Allowed"
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    @action(detail=False, methods=['GET'], url_path='deck_cards/(?P<deck_id>\d+)')
    def deck_cards(self, request, deck_id=None):
        queryset = TagToCard.objects.filter(deck_id=deck_id)
        serializer = TagToCardSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path='tags/(?P<tag_id>\d+)')
    def deck_cards(self, request, tag_id=None):
        queryset = TagToCard.objects.filter(tag_id=tag_id)
        serializer = TagToCardSerializer(queryset, many=True)
        return Response(serializer.data)



class PDFUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        # file_obj는 클라이언트에서 업로드한 파일을 나타내는 InMemoryUploadedFile 객체
        file_obj = request.data['file']
        deck_id = request.data['deckId']
        pdf_data = file_obj.read()
        doc = fitz.open("pdf", pdf_data)
        text = ""
        for page in doc:
            text += page.get_text()
        sendGPT(text,deck_id)
        return Response(status=status.HTTP_200_OK)


def sendGPT(text,deckId):
    chunk_size = 4096  

    responses = ""

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        
        if i + chunk_size < len(text):
            try:
                last_period = chunk.rindex(".")
                chunk = chunk[:last_period+1]
            except ValueError:
                pass

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "assistant", 
                "content": "Based on the information I send, please make a flash card according to the format and guidelines\n" +
                '''
                Guidelines:
                Make flashcards only on the most important information.
                Make sure the questions are clear and easy to understand
                Make the answers very concise and about a single concept or fact \n''' +
                '''
                Format:
                Create the anki flash card in the following format.
                By default, The front of the card is written in plain text. 
                For example, question:answer '''},
                {"role": "user", "content": chunk},
            ]
        )
        responses="".join((responses,completion.choices[0].message.content))

    for response in responses.split('\n'):
        question, answer = response.split(':', 1)      
        card = Card(question=question.strip(), answer=answer.strip(), cardListId=deckId)
        card.save()

class KakaoLoginView(APIView):
    def post(self, request):
        kakao_token = request.data.get('kakao_token', None)
        if kakao_token is None:
            return Response({"error": "No kakao_token provided"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {kakao_token}"}
        ).json()

        kakao_id = user_info.get('id')
        email = user_info.get('kakao_account').get('email')
        nickname = user_info.get('properties').get('nickname')

        user, created = User.objects.get_or_create(kakao_id=kakao_id, defaults={'emailAddress': email, 'nickname': nickname})

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)