from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_userprofile_age_userprofile_avatar_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]



