# conftest.py
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import News, Comment

User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def users_login_url():
    return reverse('users:login')


@pytest.fixture
def users_signup_url():
    return reverse('users:signup')


@pytest.fixture
def users_logout_url():
    return reverse('users:logout')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст',)


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_redirect_url(news_detail_url):
    return f'{news_detail_url}#comments'


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def expected_edit_redirect_url(edit_url, users_login_url):
    return f'{users_login_url}?next={edit_url}'


@pytest.fixture
def expected_delete_redirect_url(delete_url, users_login_url):
    return f'{users_login_url}?next={delete_url}'


@pytest.fixture
def news_sets():
    today = datetime.today().date()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments_sets(news, not_author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=not_author,
            text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
