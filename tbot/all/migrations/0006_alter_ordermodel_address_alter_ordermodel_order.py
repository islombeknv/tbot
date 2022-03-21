# Generated by Django 4.0.2 on 2022-03-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0005_remove_ordermodel_p_id_remove_ordermodel_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='order',
            field=models.CharField(blank=True, choices=[('Tasdiqlanmagan', 'Tasdiqlanmagan'), ('Tasdiqlandi', 'Tasdiqlandi'), ('Yuborildi', 'Yuborildi'), ('Yetkazildi', 'Yetkazildi')], default='Tasdiqlanmagan', max_length=50),
        ),
    ]