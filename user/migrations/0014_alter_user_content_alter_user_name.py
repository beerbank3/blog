# Generated by Django 4.2.3 on 2023-07-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_user_content_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='guest_62509653', max_length=50, unique=True),
        ),
    ]
