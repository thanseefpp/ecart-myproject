# Generated by Django 3.1.1 on 2020-10-16 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0014_auto_20201011_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='payment_Cod',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
