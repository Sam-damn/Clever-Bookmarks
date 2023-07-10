# Generated by Django 4.2.3 on 2023-07-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=300)),
                ('tags', models.CharField(max_length=600)),
                ('domain', models.CharField(default='', max_length=300)),
                ('content', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('isCommitted', models.BooleanField()),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]