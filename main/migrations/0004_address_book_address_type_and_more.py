# Generated by Django 4.2.7 on 2023-11-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_menu_rest_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='address_book',
            name='address_type',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='address_book',
            unique_together={('cust_id', 'address_type')},
        ),
    ]