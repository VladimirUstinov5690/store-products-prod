# Generated by Django 3.2.13 on 2024-10-13 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverification',
            options={'verbose_name': 'Email-верификация', 'verbose_name_plural': 'Верификация'},
        ),
    ]
