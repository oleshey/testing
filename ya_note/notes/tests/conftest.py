# notes/tests/conftest.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note


NOTE_SLUG = 'zagolovok'

NOTES_HOME_URL = reverse('notes:home')
NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_SUCCESS_URL = reverse('notes:success')
USERS_LOGIN_URL = reverse('users:login')
USERS_LOGOUT_URL = reverse('users:logout')
USERS_SIGNUP_URL = reverse('users:signup')

NOTES_DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
NOTES_EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
NOTES_DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))

REDIRECT_NOTES_DETAIL_URL = f'{USERS_LOGIN_URL}?next={NOTES_DETAIL_URL}'
REDIRECT_NOTES_EDIT_URL = f'{USERS_LOGIN_URL}?next={NOTES_EDIT_URL}'
REDIRECT_NOTES_DELETE_URL = f'{USERS_LOGIN_URL}?next={NOTES_DELETE_URL}'
REDIRECT_NOTES_ADD_URL = f'{USERS_LOGIN_URL}?next={NOTES_ADD_URL}'
REDIRECT_NOTES_SUCCESS_URL = f'{USERS_LOGIN_URL}?next={NOTES_SUCCESS_URL}'
REDIRECT_NOTES_LIST_URL = f'{USERS_LOGIN_URL}?next={NOTES_LIST_URL}'

User = get_user_model()


class BaseTestData(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Не Автор')
        cls.author_client = cls.client_class()
        cls.author_client.force_login(cls.author)
        cls.reader_client = cls.client_class()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=NOTE_SLUG,
            author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
