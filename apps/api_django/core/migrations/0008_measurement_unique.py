from django.db import migrations


def deduplicate_measurements(apps, schema_editor):
    Measurement = apps.get_model('core', 'Measurement')
    seen = set()
    for m in Measurement.objects.order_by('id').all():
        key = (m.proyecto_id, m.periodo)
        if key in seen:
            m.delete()
        else:
            seen.add(key)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_project_geo'),
    ]

    operations = [
        migrations.RunPython(deduplicate_measurements, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together={('proyecto', 'periodo')},
        ),
    ]


