# Generated by Django 5.1.3 on 2024-11-18 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object_detection', '0002_doctors_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=200)),
                ('r_pass', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='doctors',
            name='image',
            field=models.ImageField(default='images/anonim.png', upload_to='images'),
        ),
    ]
