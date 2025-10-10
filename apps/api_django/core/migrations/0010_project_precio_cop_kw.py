from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_project_image_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='precio_cop_kw',
            field=models.DecimalField(blank=True, decimal_places=2, default=750, max_digits=12, null=True),
        ),
    ]


