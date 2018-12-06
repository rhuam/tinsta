from pandas import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Puppy, UserFace, UserInsta, UserTinder, People, PhotosPeople
# from .serializers import PuppySerializer
from .serializers import UserFaceSerializer, UserInstaSerializer, UserTinderSerializer, PeopleSerializer, \
    PhotosPeopleSerializer, SessionSerializer
from api.tinder_master import tinder_api
from api.tinder_master import insta_follow
from datetime import datetime


@api_view(['GET', 'POST'])
def index(request):
    return Response({'mensagem': 'Bem vindo'}, status=status.HTTP_200_OK)


## FACEBOOK
@api_view(['POST'])
def post_login_facebook_tinder(request):
    try:
        user = UserFace.objects.get(name=request.data.get('name'))

        data = {
            'name': user.name,
            'password': request.data.get('password'),
        }
        data['user_id'], data['token'] = tinder_api.facebook_conection(request.data.get('name'),
                                                                       request.data.get('password'))
        data['user_tinder'] = create_user_tinder(data['user_id'], data['token'])

        serializer = UserFaceSerializer(data=data)
        if serializer.is_valid():
            serializer.update(user, data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except UserFace.DoesNotExist:
        data = {
            'name': request.data.get('name'),
            'password': request.data.get('password'),
        }
        data['user_id'], data['token'] = tinder_api.facebook_conection(request.data.get('name'),
                                                                       request.data.get('password'))
        data['user_tinder'] = create_user_tinder(data['user_id'], data['token'])

        serializer = UserFaceSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except tinder_api.fb_auth_token.FacebookErro as erro:
        return Response(erro, status=status.HTTP_400_BAD_REQUEST)

    except tinder_api.TinderErro as erro:
        return Response(erro, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_fb(request, pk):
    try:
        user = UserFace.objects.get(user_id=pk)
        serializer = UserFaceSerializer(user)
        return Response(serializer.data)
    except UserFace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


###### INSTAGRAM
@api_view(['GET'])
def get_user_instagram(request, pk):
    try:
        user = UserInsta.objects.get(user_id=pk)
        serializer = UserInstaSerializer(user)
        return Response(serializer.data)
    except UserInsta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def post_login_instagram(request):
    try:
        user = UserInsta.objects.get(name=request.data.get('name'))
        data = {
            'name': request.data.get('name'),
            'password': request.data.get('password'),
            'session': insta_follow.instagram_conection(request.data.get('name'), request.data.get('password'))
        }

        serializer = UserInstaSerializer(user)
        if serializer.is_valid():
            serializer.update(user, data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except UserInsta.DoesNotExist:
        data = {
            'name': request.data.get('name'),
            'password': request.data.get('password'),
            'user_id': insta_follow.get_id(request.data.get('name')),
            'session': insta_follow.instagram_conection(request.data.get('name'), request.data.get('password'))
        }

        serializer = UserInstaSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except insta_follow.InstagramErro as erro:
        return Response(erro, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_follow_instagram(request):
    tinder = request.data.get('tinder')
    instagram = request.data.get('instagram')
    try:
        user_insta = UserInsta.objects.get(user_id=instagram['user_id'])
        insta_follow.follow(user_insta.session, instagram['user_follow_id'])

        user_tinder = UserTinder.objects.get(user_id=tinder['user_tinder_id'])
        tinder_api.like(tinder['user_tinder_like'], user_tinder.token)

        return Response(status=status.HTTP_200_OK)
    except UserInsta.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except UserTinder.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except insta_follow.InstagramErro:
        user_insta = UserInsta.objects.get(user_id=instagram['user_id'])
        user_insta.session = insta_follow.instagram_conection(user_insta.name, user_insta.password)


@api_view(['POST'])
def post_dislike_tinder(request):
    try:
        user_tinder = UserTinder.objects.get(user_id=request.data.get('user_tinder_id'))
        for u in request.data.get('dislike'):
            tinder_api.dislike(u, user_tinder.token)
    except UserTinder.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


######### TINDER

def create_user_tinder(fb_user_id, fb_token):
    req = tinder_api.tinder_conection(fb_token, fb_user_id)

    data = {}
    data['name'] = req['user']['full_name']
    data['user_id'] = req['user']['_id']
    data['token'] = req['token']
    data['gender_filter'] = req['user']['gender_filter']
    data['max_ditance'] = int(round(req['user']['distance_filter'] * 1.609344))
    data['min_age'] = req['user']['age_filter_min']
    data['max_age'] = req['user']['age_filter_max']
    data['photo'] = req['user']['photos'][0]['url']

    nasc = datetime.strptime(req['user']['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    hoje = datetime.now()
    data['age'] = int(round((hoje - nasc).days / 365))

    return data


@api_view(['POST'])
def post_update_tinder(request, pk):
    try:
        user = UserInsta.objects.get(user_id=pk)

        data = {}

        data['gender_filter'] = request['gender_filter']
        data['max_ditance'] = int(round(request['distance_filter'] * 1.609344))
        data['min_age'] = request['min_age']
        data['max_age'] = request['max_age']

        serializer = UserInstaSerializer(user)
        if serializer.is_valid():
            serializer.update(user, data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserInsta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


##### PEOPLE SEARCH

def insta_search(results):
    insta_user = ""

    if 'instagram' in results.keys():
        insta_user = results['instagram']['username']
    else:
        bioList = results['bio'].split()

        for b in range(len(bioList)):
            if 'insta' in bioList[b]:
                insta_user = bioList[b + 1]
            elif '@' in bioList[b]:
                insta_user = bioList[b]
    insta_user = insta_user.replace('@', '')
    if insta_user == '':
        return '', ''
    return insta_user, insta_follow.get_id(insta_user)


@api_view(['GET'])
def get_user_people(request, pk):
    try:
        datas = []
        for i in range(3):
            user = UserTinder.objects.get(user_id=pk)

            if request.method == 'GET':
                response = tinder_api.get_recommendations(user.token)

                for results in response['results']:
                    data = {}
                    insta_info = insta_search(results)

                    if insta_info[0] != '':
                        data = {
                            'id': results['_id'],
                            'name': results['name'],
                            'distance': int(round(results['distance_mi'] * 1.609344)),
                            'bio': results['bio'],
                            'jobs': results['jobs'],
                            'schools': results['schools'],
                        }

                        nasc = datetime.strptime(results['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        hoje = datetime.now()
                        data['age'] = int(round((hoje - nasc).days / 365))
                        data['insta_name'], data['insta_id'] = insta_info
                        data['photos'] = []

                        # for photo in results['photos']:
                        #     ph = {
                        #         'url' : photo['url']
                        #     }
                        #     data['photos'].append(ph)

                        if 'instagram' in results.keys():
                            for photo in results['instagram']['photos']:
                                ph = {
                                    'url': photo['image'],
                                    'link': photo['link'],
                                    'ts': photo['ts']
                                }
                                data['photos'].append(ph)
                        datas.append(data)
            return Response({'quantidade': len(datas), 'response': datas})
    except UserTinder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
