# Generated by Django 3.1.3 on 2020-11-19 16:28

from django.db import migrations


def create_codelists_for_drafts(apps, schema_editor):
    Codelist = apps.get_model("codelists", "Codelist")
    DraftCodelist = apps.get_model("builder", "DraftCodelist")

    for draft in DraftCodelist.objects.all():
        draft.codelist = Codelist.objects.create(
            name=draft.name,
            slug=draft.slug,
            user=draft.owner,
            coding_system_id=draft.coding_system_id,
        )
        draft.save()


class Migration(migrations.Migration):

    dependencies = [
        ("builder", "0007_draftcodelist_codelist"),
    ]

    operations = [migrations.RunPython(create_codelists_for_drafts)]