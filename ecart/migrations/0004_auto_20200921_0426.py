# Generated by Django 3.1.1 on 2020-09-21 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0003_auto_20200920_1612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='arrtribute',
            new_name='attribute',
        ),
    ]
