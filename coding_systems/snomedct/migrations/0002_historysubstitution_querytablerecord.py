# Generated by Django 3.0.5 on 2020-06-12 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snomedct', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryTableRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provenance', models.IntegerField()),
                ('subtype', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='snomedct.Concept')),
                ('supertype', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='snomedct.Concept')),
            ],
        ),
        migrations.CreateModel(
            name='HistorySubstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_concept_status', models.CharField(max_length=18)),
                ('new_concept_status', models.CharField(max_length=18)),
                ('path', models.CharField(max_length=255)),
                ('is_ambiguous', models.BooleanField()),
                ('iterations', models.IntegerField()),
                ('old_concept_fsn', models.CharField(max_length=255)),
                ('old_concept_fsn_tagcount', models.IntegerField()),
                ('new_concept_fsn', models.CharField(max_length=255)),
                ('new_concept_fsn_tagcount', models.IntegerField()),
                ('tlh_identical_flag', models.BooleanField()),
                ('fsn_tagless_identical_flag', models.BooleanField()),
                ('fsn_tag_identical_flag', models.BooleanField()),
                ('new_concept', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='snomedct.Concept')),
                ('old_concept', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='snomedct.Concept')),
            ],
        ),
    ]
