from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('governance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityenergy',
            name='nombre',
            field=models.CharField(default='Comunidad Energia', max_length=255),
        ),
        migrations.AddField(
            model_name='communityenergy',
            name='ciudad',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='communityenergy',
            name='barrio',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='communityenergy',
            name='historia',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='communityenergy',
            name='fotos_miembros',
            field=models.JSONField(blank=True, default=list),
        ),
    ]


