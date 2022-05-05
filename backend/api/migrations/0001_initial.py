# Generated by Django 3.1.8 on 2022-05-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('age', models.IntegerField(verbose_name='age')),
            ],
            options={
                'verbose_name': 'UserTable',
                'verbose_name_plural': 'UserTable',
                'db_table': 'user',
                'ordering': ['id'],
            },
        ),
    ]
