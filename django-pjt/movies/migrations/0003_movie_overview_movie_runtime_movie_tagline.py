# Generated by Django 4.2.13 on 2024-05-21 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='overview',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='tagline',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
