# Generated by Django 3.2.9 on 2021-11-01 18:54

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20211101_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', wagtail.core.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Футер',
                'verbose_name_plural': 'Футеры',
            },
        ),
    ]
