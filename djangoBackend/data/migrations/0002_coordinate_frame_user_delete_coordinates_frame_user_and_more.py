# Generated by Django 4.1.7 on 2023-03-18 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField(help_text='Enter the width (x value) for the coordinate: ')),
                ('y', models.FloatField(help_text='Enter the height (y value) for the coordinate: ')),
                ('z', models.FloatField(help_text='Enter the depth (z value) for the coordinate: ')),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Enter name of frame: ', max_length=100)),
                ('description', models.TextField(help_text='Enter description of frame: ', max_length=1000)),
                ('date_created', models.DateTimeField(help_text='Enter date and time that this frame was created: ')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(help_text='Enter user first name: ', max_length=100)),
                ('last_name', models.TextField(help_text='Enter user last name: ', max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Coordinates',
        ),
        migrations.AddField(
            model_name='frame',
            name='user',
            field=models.ForeignKey(help_text='Enter the id of the user who owns this frame: ', on_delete=django.db.models.deletion.CASCADE, to='data.user'),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='frame',
            field=models.ForeignKey(help_text='Enter the id of the frame corresponding to this coordinate: ', on_delete=django.db.models.deletion.CASCADE, to='data.frame'),
        ),
    ]