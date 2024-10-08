# Generated by Django 5.1.1 on 2024-10-08 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_servicecategory_serviceproduct_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serviceproduct',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serviceproductsupplier',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
