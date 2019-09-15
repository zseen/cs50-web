# Generated by Django 2.0.3 on 2019-09-08 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190908_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='category',
        ),
        migrations.AddField(
            model_name='dinnerplatter',
            name='category',
            field=models.CharField(default='Dinner platter', max_length=64),
        ),
        migrations.AddField(
            model_name='pasta',
            name='category',
            field=models.CharField(default='Pasta', max_length=64),
        ),
        migrations.AddField(
            model_name='regularpizza',
            name='category',
            field=models.CharField(default='Regular pizza', max_length=64),
        ),
        migrations.AddField(
            model_name='salad',
            name='category',
            field=models.CharField(default='Salad', max_length=64),
        ),
        migrations.AddField(
            model_name='sicilianpizza',
            name='category',
            field=models.CharField(default='Sicilian pizza', max_length=64),
        ),
        migrations.AddField(
            model_name='sub',
            name='category',
            field=models.CharField(default='Sub', max_length=64),
        ),
        migrations.AddField(
            model_name='topping',
            name='category',
            field=models.CharField(default='Topping', max_length=64),
        ),
    ]