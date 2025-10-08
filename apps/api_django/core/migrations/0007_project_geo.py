from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_project_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lat',
            field=models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6),
        ),
        migrations.AddField(
            model_name='project',
            name='lng',
            field=models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6),
        ),
        migrations.AddField(
            model_name='project',
            name='descripcion',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]


