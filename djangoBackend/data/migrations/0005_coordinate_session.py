# Generated by Django 4.1.7 on 2023-04-05 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_rename_involvedinsession_involvedin_coordinate_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordinate',
            name='session',
            field=models.ForeignKey(default=2, help_text='Enter session this coordinate belongs to: ', on_delete=django.db.models.deletion.CASCADE, to='data.session'),
            preserve_default=False,
        ),
    ]