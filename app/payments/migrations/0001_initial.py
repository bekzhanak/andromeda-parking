# Generated by Django 5.1.7 on 2025-03-30 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20)),
                ('receipt', models.CharField(max_length=50, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('note', models.CharField(blank=True, max_length=255)),
                ('provider', models.CharField(choices=[('KASSA24', 'Kassa24')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('provider', models.CharField(choices=[('KASSA24', 'Kassa24')], max_length=30)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('amount_applied', models.DecimalField(decimal_places=2, max_digits=10)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='payments.payment')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='attempt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='payments.paymentattempt'),
        ),
        migrations.CreateModel(
            name='PaymentAttemptDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('payment_attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to='payments.paymentattempt')),
            ],
        ),
    ]
