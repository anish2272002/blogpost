# Generated by Django 4.0.4 on 2022-05-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='../static/img6Q.png', upload_to='profile'),
        ),
    ]