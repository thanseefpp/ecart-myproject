# Generated by Django 3.1.1 on 2020-10-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0012_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='payment_stauts',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
