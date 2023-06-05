# Generated by Django 4.0.4 on 2023-05-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nid', models.IntegerField(default=0)),
                ('headimage', models.ImageField(blank=True, upload_to='pics')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, max_length=100)),
                ('body', models.TextField()),
                ('teaser', models.TextField(blank=True, verbose_name='teaser')),
                ('created', models.DateField()),
                ('pub_date', models.DateField()),
                ('categories', models.ManyToManyField(to='products.product')),
            ],
        ),
    ]
