# Generated by Django 4.0.3 on 2022-04-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_bookofmonth_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Выберите жанр(ы) книги', to='catalog.genre'),
        ),
    ]
