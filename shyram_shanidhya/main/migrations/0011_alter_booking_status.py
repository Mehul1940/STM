# Generated by Django 5.1.7 on 2025-03-21 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_facility_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='processing', max_length=10),
        ),
    ]
