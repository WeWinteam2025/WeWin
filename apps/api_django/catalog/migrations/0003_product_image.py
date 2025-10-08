from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_b2border'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]


