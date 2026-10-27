# test_content.py
from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, news_sets, home_url):
    response = client.get(home_url)
    assert len(response.context['object_list']
               ) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url):
    response = client.get(home_url)
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news, comments_sets, news_detail_url):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, news, news_detail_url):
    response = client.get(news_detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news, news_detail_url):
    response = author_client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
