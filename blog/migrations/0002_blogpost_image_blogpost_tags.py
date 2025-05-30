# Generated by Django 5.2 on 2025-05-07 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.CharField(default='Uncategorized', help_text='Enter comma-separated tags', max_length=200),
            preserve_default=False,
        ),
    ]
