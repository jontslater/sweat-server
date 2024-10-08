# Generated by Django 4.1.3 on 2024-09-02 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sweatapi', '0004_remove_workout_workout_type_workout_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='type',
        ),
        migrations.AddField(
            model_name='workout',
            name='workout_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='sweatapi.workouttype'),
            preserve_default=False,
        ),
    ]
