# Generated by Django 4.2.3 on 2023-07-24 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='guest_94266633', max_length=50, unique=True),
        ),
    ]
