# Generated by Django 4.1.4 on 2023-01-13 07:09

from django.db import migrations
import ldapdb.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_ldapuser_uidnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldapuser',
            name='password',
            field=ldapdb.models.fields.CharField(max_length=200, null=True),
        ),
    ]
