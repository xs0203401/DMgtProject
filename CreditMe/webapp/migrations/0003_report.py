# Generated by Django 2.1.2 on 2018-11-07 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20181105_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sql_string', models.CharField(default='select 0', max_length=2048)),
            ],
        ),
    ]
