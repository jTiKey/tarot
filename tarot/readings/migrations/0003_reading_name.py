# Generated by Django 2.0.9 on 2018-10-18 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0002_auto_20181018_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='name',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
    ]
