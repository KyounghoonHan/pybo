# Generated by Django 3.1.3 on 2021-12-06 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0007_auto_20211202_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(default='qna', max_length=200),
        ),
    ]