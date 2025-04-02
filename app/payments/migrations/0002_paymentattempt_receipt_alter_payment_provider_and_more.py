# Generated by Django 5.1.7 on 2025-04-02 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentattempt',
            name='receipt',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='provider',
            field=models.CharField(choices=[('KASSA24', 'Kassa24'), ('KASPI', 'Kaspi')], max_length=30),
        ),
        migrations.AlterField(
            model_name='paymentattempt',
            name='provider',
            field=models.CharField(choices=[('KASSA24', 'Kassa24'), ('KASPI', 'Kaspi')], max_length=30),
        ),
    ]
