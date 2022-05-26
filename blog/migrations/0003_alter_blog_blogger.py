# Generated by Django 4.0.4 on 2022-05-26 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_blog_img_blog_imgthumb_alter_blog_blogger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blogger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL),
        ),
    ]