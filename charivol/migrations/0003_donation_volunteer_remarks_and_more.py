# Generated by Django 5.2.1 on 2025-06-09 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charivol', '0002_donationarea_area_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='volunteer_remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donation_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charivol.donor'),
        ),
    ]
