# Generated by Django 4.1 on 2022-09-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_image_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='descfuncao',
            field=models.CharField(default='n/a', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='descsecao',
            field=models.CharField(default='n/a', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(default='bor@123', max_length=50),
        ),
    ]
