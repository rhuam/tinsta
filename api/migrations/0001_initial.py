# Generated by Django 2.1.3 on 2018-12-06 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.PositiveSmallIntegerField()),
                ('distance', models.PositiveSmallIntegerField()),
                ('bio', models.TextField()),
                ('jobs', models.CharField(max_length=255)),
                ('schools', models.CharField(max_length=255)),
                ('insta_name', models.CharField(max_length=255)),
                ('insta_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhotosPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_id', models.CharField(max_length=255)),
                ('photo_url', models.CharField(max_length=255)),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.People')),
            ],
        ),
        migrations.CreateModel(
            name='Puppy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('breed', models.CharField(max_length=255, null=True)),
                ('color', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserFace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInsta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
                ('session', models.BinaryField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTinder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender_filter', models.IntegerField()),
                ('max_ditance', models.IntegerField()),
                ('min_age', models.IntegerField()),
                ('max_age', models.IntegerField()),
                ('photo', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fb_user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_tinder', to='api.UserFace')),
            ],
        ),
    ]
