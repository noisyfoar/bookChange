# Generated by Django 4.0.4 on 2022-04-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_chat_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='trade_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chat',
            name='trade_owner',
            field=models.BooleanField(default=False),
        ),
    ]