# Generated by Django 5.1.4 on 2024-12-21 05:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='my_app.post'),
        ),
    ]