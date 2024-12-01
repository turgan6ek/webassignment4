from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post

class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Content', author=self.user.username)

    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        response = self.client.post('/api/posts/', {
            'title': 'New Post',
            'content': 'New Content',
            'author': self.user.username,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
