from rest_framework import serializers
from .models import UserFace, UserInsta, UserTinder, People, PhotosPeople


class UserTinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTinder
        fields = (
            'name', 'fb_user_id', 'user_id', 'token', 'age', 'gender_filter', 'max_ditance', 'min_age', 'max_age',
            'photo', 'created_at', 'updated_at')


class UserFaceSerializer(serializers.ModelSerializer):
    user_tinder = UserTinderSerializer()

    class Meta:
        model = UserFace
        fields = ('name', 'password', 'user_id', 'token', 'created_at', 'updated_at', 'user_tinder')

    def create(self, validated_data):
        user_tinder_data = validated_data.pop('user_tinder')
        user_fb = UserFace.objects.create(**validated_data)
        UserTinder.objects.update_or_create(fb_user_id=user_fb, **user_tinder_data)
        return user_fb

    def update(self, instance, validated_data):
        instance.password = validated_data['password']
        instance.token = validated_data['token']
        user_tinder_data = validated_data.pop('user_tinder')
        instance.user_tinder.name = user_tinder_data['name']
        instance.user_tinder.user_id = user_tinder_data['user_id']
        instance.user_tinder.token = user_tinder_data['token']
        instance.user_tinder.gender_filter = user_tinder_data['gender_filter']
        instance.user_tinder.max_ditance = user_tinder_data['max_ditance']
        instance.user_tinder.min_age = user_tinder_data['min_age']
        instance.user_tinder.max_age = user_tinder_data['max_age']
        instance.user_tinder.photo = user_tinder_data['photo']
        instance.user_tinder.age = user_tinder_data['age']
        instance.user_tinder.save()
        instance.save()
        return instance


class UserInstaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInsta
        fields = ('name', 'password', 'user_id', 'token', 'urlgen', 'mid', 'created_at', 'updated_at')


class PhotosPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotosPeople
        fields = ('photo_id', 'photo_url')


class PeopleSerializer(serializers.ModelSerializer):
    photos = PhotosPeopleSerializer(many=True)

    class Meta:
        model = People
        fields = ('name', 'age', 'gender', 'distance', 'bio', 'jobs', 'schools', 'photos')
