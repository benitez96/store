# Generated by Django 4.1.4 on 2023-01-09 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='street',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='lastname',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='neighborhood',
            field=models.CharField(default='lastname', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='street_number',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]