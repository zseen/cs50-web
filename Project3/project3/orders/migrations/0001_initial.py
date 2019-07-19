# Generated by Django 2.0.3 on 2019-07-19 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='SOME STRING', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='OnePriceFood',
            fields=[
                ('food_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.Food')),
                ('price', models.DecimalField(decimal_places=2, default='SOME STRING', max_digits=4, null=True)),
            ],
            bases=('orders.food',),
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('food_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.Food')),
            ],
            bases=('orders.food',),
        ),
        migrations.CreateModel(
            name='TwoPriceFood',
            fields=[
                ('food_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.Food')),
                ('smallPrice', models.DecimalField(decimal_places=2, default='SOME STRING', max_digits=4, null=True)),
                ('largePrice', models.DecimalField(decimal_places=2, default='SOME STRING', max_digits=4, null=True)),
            ],
            bases=('orders.food',),
        ),
        migrations.CreateModel(
            name='DinnerPlatter',
            fields=[
                ('twopricefood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.TwoPriceFood')),
            ],
            bases=('orders.twopricefood',),
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('onepricefood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.OnePriceFood')),
            ],
            bases=('orders.onepricefood',),
        ),
        migrations.CreateModel(
            name='RegularPizza',
            fields=[
                ('twopricefood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.TwoPriceFood')),
            ],
            bases=('orders.twopricefood',),
        ),
        migrations.CreateModel(
            name='Salad',
            fields=[
                ('onepricefood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.OnePriceFood')),
            ],
            bases=('orders.onepricefood',),
        ),
        migrations.CreateModel(
            name='SicilianPizza',
            fields=[
                ('twopricefood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.TwoPriceFood')),
            ],
            bases=('orders.twopricefood',),
        ),
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('twopricefood_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.TwoPriceFood')),
            ],
            bases=('orders.twopricefood',),
        ),
    ]
