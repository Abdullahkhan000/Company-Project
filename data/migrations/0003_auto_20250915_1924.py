from django.db import migrations
from django.utils.text import slugify


def forwards(apps, schema_editor):
    Birth = apps.get_model("data", "Birth")
    for obj in Birth.objects.filter(slug__isnull=True):
        # Auto-generate slug from name + id (to keep uniqueness per date)
        base_slug = slugify(obj.name) or "birth"
        obj.slug = f"{base_slug}-{obj.id}"
        obj.save()


def backwards(apps, schema_editor):
    # Optionally clear slugs if rolling back
    Birth = apps.get_model("data", "Birth")
    for obj in Birth.objects.all():
        obj.slug = None
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0002_birth_slug"),  # replace with your latest migration
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
