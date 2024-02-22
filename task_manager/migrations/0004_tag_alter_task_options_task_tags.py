# Generated by Django 4.2 on 2024-02-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0003_alter_task_is_completed"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["deadline", "is_completed"]},
        ),
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(related_name="tasks", to="task_manager.tag"),
        ),
    ]
