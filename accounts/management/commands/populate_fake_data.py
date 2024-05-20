import random
from faker import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Position, Profile, Gender
from task_manager.models import Task, Priority, TaskType, Tag

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **kwargs) -> None:
        # Create positions
        positions = ["Developer", "Designer", "QA Engineer", "Project Manager"]
        for position_name in positions:
            position, created = Position.objects.get_or_create(
                name=position_name
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created position: {position.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Position already exists: {position.name}"
                    )
                )

        # Create tags
        tags = ["Development", "Design", "Testing", "Documentation"]
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created tag: {tag.name}")
                )
            else:
                self.stdout.write(self.style.WARNING(
                    f"Tag already exists: {tag.name}")
                )

        # Create task types
        task_types = ["Bug", "Feature", "Improvement"]
        for task_type_name in task_types:
            task_type, created = TaskType.objects.get_or_create(
                name=task_type_name
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created task type: {task_type.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Task type already exists: {task_type.name}"
                    )
                )

        # Create users
        positions = list(Position.objects.all())
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@example.com"
            password = "password123"
            position = random.choice(positions)

            user = get_user_model().objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                position=position,
            )

            Profile.objects.create(
                id=user.id,
                user=user,
                avatar=fake.image_url(),
                gender=random.choice([choice[0] for choice in Gender.choices]),
                date_of_birth=fake.date_of_birth(),
                info=fake.text(max_nb_chars=255),
            )

            # Create tasks for each user
            for _ in range(random.randint(1, 5)):
                name = fake.sentence(
                    nb_words=6, variable_nb_words=True, ext_word_list=None
                )
                description = fake.text(max_nb_chars=200)
                random_days = fake.random_int(min=1, max=30)
                deadline = timezone.now() + timezone.timedelta(
                    days=random_days
                )
                is_completed = fake.boolean(chance_of_getting_true=50)
                priority = random.choice(
                    [choice[0] for choice in Priority.choices]
                )
                task_type = TaskType.objects.get(
                    name=random.choice(task_types)
                )
                tags = Tag.objects.order_by("?")[: random.randint(1, 3)]

                task = Task.objects.create(
                    name=name,
                    description=description,
                    deadline=deadline,
                    is_completed=is_completed,
                    priority=priority,
                    task_type=task_type,
                )

                task.assignees.add(user)
                task.tags.add(*tags)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with fake data"
            )
        )
