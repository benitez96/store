# Generated by Django 4.1.4 on 2023-01-06 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xs', models.PositiveSmallIntegerField(default=0)),
                ('s', models.PositiveSmallIntegerField(default=0)),
                ('m', models.PositiveSmallIntegerField(default=0)),
                ('l', models.PositiveSmallIntegerField(default=0)),
                ('xl', models.PositiveSmallIntegerField(default=0)),
                ('xxl', models.PositiveSmallIntegerField(default=0)),
                ('xxxl', models.PositiveSmallIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='store_app.product')),
            ],
        ),
    ]
