# Generated by Django 3.2.2 on 2021-05-09 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('door', '0002_alter_door_door_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='door_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
