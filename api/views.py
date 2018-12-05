from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Puppy, UserFace, UserInsta, UserTinder, People, PhotosPeople
# from .serializers import PuppySerializer
from .serializers import UserFaceSerializer, UserInstaSerializer, UserTinderSerializer, PeopleSerializer, \
    PhotosPeopleSerializer
from api.tinder_master import tinder_api
from api.tinder_master import insta_follow
from datetime import datetime

@api_view(['GET', 'POST'])
def index(request):
    return Response({'mensagem': 'Bem vindo'}, status=status.HTTP_200_OK)



def validar(data):
    for e in data.items():
        if (type(e[1]) is dict):
            if ('error' in e[1].keys()):
                return e[1]
    return False


# @api_view(['GET', 'DELETE', 'PUT'])
# def get_delete_update_user_fb(request, pk):
#     try:
#         user = UserFace.objects.get(pk=pk)
#     except UserFace.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = UserFaceSerializer(user)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         serializer = UserFaceSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def get_post_user_fb(request):
    if request.method == 'GET':
        users = UserFace.objects.all()
        serializer = UserFaceSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = False
        try:
            user = UserFace.objects.get(name=request.data.get('name'))
        except UserFace.DoesNotExist:
            pass

        data = {
            'name': request.data.get('name'),
            'password': request.data.get('password')
        }
        data['user_id'], data['token'] = tinder_api.facebook_conection(request.data.get('name'), request.data.get('password'))
        data['user_tinder'] = create_user_tinder(data['user_id'], data['token'])

        v = validar(data)
        if v:
            return Response(v, status=status.HTTP_400_BAD_REQUEST)

        if user:
            serializer = UserFaceSerializer(user, data=data)
        else:
            serializer = UserFaceSerializer(data=data)

        if serializer.is_valid():
            if user:
                serializer.update(user, data)
            else:
                serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###### INSTAGRAM

@api_view(['GET', 'POST'])
def get_post_user_insta(request):
    if request.method == 'GET':
        users = UserInsta.objects.all()
        serializer = UserInstaSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = False
        try:
            user = UserInsta.objects.get(name=request.data.get('name'))
        except UserInsta.DoesNotExist:
            pass

        data = {
            'name': request.data.get('name'),
            'password': request.data.get('password')
        }
        # data['user_id'], data['token'], data['sessionid'] = insta_follow.main(request.data.get('name'), request.data.get('password'), request.data.get('user_follow'))
        insta_follow.follow_2('rhuamsena', 'R3zlccBGPsXw7bVhyfeiXrKbCVCSe56h', 'IGSCf348265baf5c4d78e237429033b51703cf82faec21617c70312814d75f06a7ce%3AUIqXF1sHZ2QNv1z1sTaWYyapaWJvrUHF%3A%7B%22_auth_user_id%22%3A9292421724%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%229292421724%3AbdkysniZxZCFHL7Zr9LvWNw1Hb21jPjU%3A12233544f2c12ddaaf5ed3b51cd0a92f37df4fe96e655dfda99bd740c5249931%22%2C%22last_refreshed%22%3A1544023783.1581082344%7D',
                              '9292421724')

        print(data)

        data['user_id'], data['token'] = user.user_id, user.token
        data['urlgen'] = "123"

        # insta_follow.follow_2(request.data.get('user_follow'),user.token, user.mid, user.user_id )

        v = validar(data)
        if v:
            return Response(v, status=status.HTTP_400_BAD_REQUEST)

        if user:
            serializer = UserInstaSerializer(user, data=data)
        else:
            serializer = UserInstaSerializer(data=data)

        if serializer.is_valid():
            if user:
                serializer.update(user, data)
            else:
                serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######### TINDER

def create_user_tinder(fb_user_id, fb_token):
    req = tinder_api.tinder_conection(fb_token, fb_user_id)

    v = validar({'response': req})
    if v:
        return v

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


@api_view(['GET'])
def get_post_user_tinder(request):
    if request.method == 'GET':
        users = UserTinder.objects.all()
        serializer = UserTinderSerializer(users, many=True)
        return Response(serializer.data)

    # if request.method == 'POST':
    #     try:
    #         user = UserFace.objects.get(name__iexact=request.data.get('fb_user_id'))
    #         user.user_id, user.token = tinder_api.facebook_conection(user.name, user.password)
    #
    #         validar(user.__dict__)
    #
    #         serializer = UserInstaSerializer(user, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    #     except UserInsta.DoesNotExist:
    #
    #         fb_token = request.data.get('fb_token')
    #         fb_user_id = request.data.get('fb_user_id')
    #
    #         req = tinder_api.tinder_conection(fb_token, fb_user_id)
    #
    #         print(req)
    #
    #         v = validar({'response': req})
    #         if not v == None:
    #             return v
    #
    #         data = {}
    #         data['name'] = req['user']['full_name']
    #         data['user_id'] = req['user']['_id']
    #         data['token'] = req['token']
    #         data['gender_filter'] = req['user']['gender_filter']
    #         data['max_ditance'] = int(round(req['user']['distance_filter'] * 1.609344))
    #         data['min_age'] = req['user']['age_filter_min']
    #         data['max_age'] = req['user']['age_filter_max']
    #         data['photo'] = req['user']['photos'][0]['url']
    #
    #         nasc = datetime.strptime(req['user']['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #         hoje = datetime.now()
    #         data['age'] = int(round((hoje - nasc).days / 365))
    #
    #         serializer = UserTinderSerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######### PEOPLE
# @api_view(['GET', 'DELETE', 'PUT'])
# def get_delete_update_user_people(request):
#     # try:
#     #     people = People.objects.get(pk=pk)
#     # except People.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PeopleSerializer(people)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         serializer = PeopleSerializer(people, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         people.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
def get_post_user_people(request, token):
    if request.method == 'GET':
        response = tinder_api.get_recommendations(token)
        datas = []

        for results in response['results']:
            data = {}
            data['insta_name'], data['insta_id'] = insta_search(results)

            if data['insta_name'] != '':
                data = {
                    'name': results['name'],
                    'distance': int(round(results['distance_mi'] * 1.609344)),
                    'bio': results['bio'],
                    'jobs': results['jobs'],
                    'schools': results['schools'],
                }

                nasc = datetime.strptime(results['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                hoje = datetime.now()
                data['age'] = int(round((hoje - nasc).days / 365))

                data['insta_name'], data['insta_id'] = insta_search(results)
                if data['insta_name'] != '':
                    datas.append(data)

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

        return Response({'response': datas})


@api_view(['GET','POST'])
def post_follow_user(request):

    return Response(status=status.HTTP_200_OK)
