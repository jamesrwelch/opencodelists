# Generated by Django 3.1.1 on 2020-09-28 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RawConcept",
            fields=[
                (
                    "read_code",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("C", "Current"),
                            ("E", "Extinct"),
                            ("O", "Optional"),
                            ("R", "Redundant"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "unknown_field_2",
                    models.CharField(
                        choices=[
                            ("A", "Unknown field 2: A"),
                            ("A", "Unknown field 2: N"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "another_concept",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ctv3.rawconcept",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RawTerm",
            fields=[
                (
                    "term_id",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("C", "Status: C (Current?)"),
                            ("O", "Status: O (Optional?)"),
                        ],
                        max_length=1,
                    ),
                ),
                ("name_1", models.CharField(max_length=30)),
                ("name_2", models.CharField(max_length=60, null=True)),
                ("name_3", models.CharField(max_length=198, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="TPPConcept",
            fields=[
                (
                    "read_code",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("description", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="TPPRelationship",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("distance", models.IntegerField()),
                (
                    "ancestor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="descendant_relationships",
                        to="ctv3.tppconcept",
                    ),
                ),
                (
                    "descendant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ancestor_relationships",
                        to="ctv3.tppconcept",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RawConceptTermMapping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "term_type",
                    models.CharField(
                        choices=[("P", "Preferred"), ("S", "Synonym")], max_length=1
                    ),
                ),
                (
                    "concept",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ctv3.rawconcept",
                    ),
                ),
                (
                    "term",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ctv3.rawterm"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RawConceptHierarchy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("list_order", models.CharField(max_length=2)),
                (
                    "child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parent_links",
                        to="ctv3.rawconcept",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child_links",
                        to="ctv3.rawconcept",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="rawconcept",
            name="children",
            field=models.ManyToManyField(
                related_name="parents",
                through="ctv3.RawConceptHierarchy",
                to="ctv3.RawConcept",
            ),
        ),
        migrations.AddField(
            model_name="rawconcept",
            name="terms",
            field=models.ManyToManyField(
                related_name="concepts",
                through="ctv3.RawConceptTermMapping",
                to="ctv3.RawTerm",
            ),
        ),
    ]
