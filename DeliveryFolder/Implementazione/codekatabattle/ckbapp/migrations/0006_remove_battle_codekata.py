# Generated by Django 4.2.9 on 2024-01-28 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ckbapp', '0005_alter_battle_codekata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='codeKata',
        ),
    ]