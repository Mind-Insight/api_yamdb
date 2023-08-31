# Generated by Django 3.2 on 2023-08-31 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230829_2044'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='#',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='Unique_review'),
        ),
    ]
