# test_logic.py
from http import HTTPStatus

from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария формы'}
BAD_WORDS_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    response = client.post(news_detail_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_user_can_create_comment(not_author_client, news_detail_url,
                                 comment_redirect_url, news, not_author):
    response = not_author_client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, comment_redirect_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.news == news
    assert comment.author == not_author
    assert comment.text == FORM_DATA['text']


def test_user_cant_use_bad_words(not_author_client, news_detail_url):
    response = not_author_client.post(news_detail_url, data=BAD_WORDS_DATA)
    form = response.context['form']
    assert not form.is_valid()
    assert 'text' in form.errors
    assert WARNING in form.errors['text']
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete_url,
                                   comment_redirect_url):
    response = author_client.delete(delete_url)
    assertRedirects(response, comment_redirect_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, edit_url, comment,
                                 comment_redirect_url):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, comment_redirect_url)
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
    assert updated_comment.text == FORM_DATA['text']


def test_user_cant_edit_comment_of_another_user(comment, not_author_client,
                                                edit_url):
    response = not_author_client.post(edit_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
    assert updated_comment.text == comment.text


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  delete_url, comment):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == comment.text
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
