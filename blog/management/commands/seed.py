from django.core.management.base import BaseCommand
from blog.models import Post
from django.contrib.auth.models import User, Group
import random

class Command(BaseCommand):
    help = 'Seed database with static posts and users'

    def handle(self, *args, **kwargs):
        # Create Groups (Roles)
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        author_group, _ = Group.objects.get_or_create(name='Author')
        reader_group, _ = Group.objects.get_or_create(name='Reader')

        # Create Users
        admin_user, created = User.objects.get_or_create(username='admin', email='admin@example.com')
        if created:
            admin_user.set_password('password')
            admin_user.save()
            admin_user.groups.add(admin_group)

        author_user, created = User.objects.get_or_create(username='author', email='author@example.com')
        if created:
            author_user.set_password('password')
            author_user.save()
            author_user.groups.add(author_group)

        reader_user, created = User.objects.get_or_create(username='reader', email='reader@example.com')
        if created:
            reader_user.set_password('password')
            reader_user.save()
            reader_user.groups.add(reader_group)

        # Create Static Posts
        if not Post.objects.exists():
            for i in range(5):
                Post.objects.create(
                    title=f"Sample Post {i+1}",
                    content=f"This is the content for Sample Post {i+1}.",
                    author='admin',
                    image=None  # Replace with a valid image path if needed
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with static posts and users.'))
