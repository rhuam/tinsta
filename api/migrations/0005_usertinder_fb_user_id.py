# Generated by Django 2.1.3 on 2018-12-04 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20181204_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertinder',
            name='fb_user_id',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fb_user_id', to='api.UserFace'),
            preserve_default=False,
        ),
    ]