# Generated by Django 5.0.7 on 2024-07-30 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Walk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('walkDate', models.DateField()),
                ('distance', models.IntegerField()),
                ('minutes', models.IntegerField()),
            ],
        ),
    ]
