# Generated by Django 4.0.4 on 2022-05-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blogger', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('datetime', models.DateTimeField()),
            ],
        ),
    ]
