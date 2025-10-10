from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_measurement_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]


