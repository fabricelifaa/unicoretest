# Generated by Django 3.1.2 on 2020-10-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField()),
                ('adress', models.TextField()),
                ('lng', models.TextField()),
                ('lat', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=250)),
                ('public_key', models.CharField(max_length=250)),
                ('ceated_date', models.DateField()),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]
