# Generated by Django 3.2.20 on 2024-08-27 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.BooleanField(default=False)),
                ('chosen_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chosen_product', to='games.product')),
                ('product1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product1', to='games.product')),
                ('product2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product2', to='games.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.user')),
            ],
        ),
    ]