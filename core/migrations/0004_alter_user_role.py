# Generated by Django 3.2.10 on 2022-04-14 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('T', 'Teacher'), ('S', 'Student')], max_length=1, null=True),
        ),
    ]
