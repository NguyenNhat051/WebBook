# Generated by Django 3.2.8 on 2021-10-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20211025_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_star',
            field=models.PositiveIntegerField(default=0),
        ),
    ]