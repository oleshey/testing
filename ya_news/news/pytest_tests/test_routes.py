# test_routes.py
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.test.client import Client

HOME_URL = pytest.lazy_fixture('home_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
USERS_LOGIN_URL = pytest.lazy_fixture('users_login_url')
USERS_SIGNUP_URL = pytest.lazy_fixture('users_signup_url')
USERS_LOGOUT_URL = pytest.lazy_fixture('users_logout_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
EXPECTED_EDIT_REDIRECT_URL = pytest.lazy_fixture('expected_edit_redirect_url')
EXPECTED_DELETE_REDIRECT_URL = pytest.lazy_fixture(
    'expected_delete_redirect_url')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    (
        (HOME_URL, Client(), HTTPStatus.OK),
        (NEWS_DETAIL_URL, Client(), HTTPStatus.OK),
        (USERS_LOGIN_URL, Client(), HTTPStatus.OK),
        (USERS_SIGNUP_URL, Client(), HTTPStatus.OK),
        (USERS_LOGOUT_URL, Client(), HTTPStatus.OK),
        (EDIT_URL, Client(), HTTPStatus.FOUND),
        (DELETE_URL, Client(), HTTPStatus.FOUND),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_and_permissions(url, client_fixture,
                                            expected_status, users_logout_url,
                                            request):
    if str(url) == users_logout_url:
        response = client_fixture.post(url)
    else:
        response = client_fixture.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_redirect_url',
    (
        (EDIT_URL, EXPECTED_EDIT_REDIRECT_URL),
        (DELETE_URL, EXPECTED_DELETE_REDIRECT_URL),
    )
)
def test_redirects_for_anonymous_client(client, url, expected_redirect_url):
    assertRedirects(client.get(url), expected_redirect_url)
