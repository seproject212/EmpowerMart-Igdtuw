# Generated by Django 5.1.2 on 2024-11-24 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_user_options_user_date_joined_user_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='business_name',
        ),
    ]