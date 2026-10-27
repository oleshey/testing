# notes/tests/test_routes.py
from http import HTTPStatus

from .conftest import (
    BaseTestData,
    NOTES_HOME_URL,
    NOTES_LIST_URL,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    NOTES_DETAIL_URL,
    NOTES_EDIT_URL,
    NOTES_DELETE_URL,
    USERS_LOGIN_URL,
    USERS_LOGOUT_URL,
    USERS_SIGNUP_URL,
    REDIRECT_NOTES_DETAIL_URL,
    REDIRECT_NOTES_EDIT_URL,
    REDIRECT_NOTES_DELETE_URL,
    REDIRECT_NOTES_ADD_URL,
    REDIRECT_NOTES_SUCCESS_URL,
    REDIRECT_NOTES_LIST_URL,
)


class TestRoutes(BaseTestData):

    def test_pages_availability(self):
        test_cases = (
            (self.client.get, NOTES_HOME_URL, HTTPStatus.OK),
            (self.client.get, USERS_SIGNUP_URL, HTTPStatus.OK),
            (self.client.get, USERS_LOGIN_URL, HTTPStatus.OK),
            (self.client.post, USERS_LOGOUT_URL, HTTPStatus.OK),
            (self.author_client.get, NOTES_LIST_URL, HTTPStatus.OK),
            (self.author_client.get, NOTES_ADD_URL, HTTPStatus.OK),
            (self.author_client.get, NOTES_SUCCESS_URL, HTTPStatus.OK),
            (self.author_client.get, NOTES_DETAIL_URL, HTTPStatus.OK),
            (self.author_client.get, NOTES_EDIT_URL, HTTPStatus.OK),
            (self.author_client.get, NOTES_DELETE_URL, HTTPStatus.OK),
            (self.reader_client.get, NOTES_DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client.get, NOTES_EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client.get, NOTES_DELETE_URL, HTTPStatus.NOT_FOUND),
            (self.client.get, NOTES_LIST_URL, HTTPStatus.FOUND),
            (self.client.get, NOTES_ADD_URL, HTTPStatus.FOUND),
            (self.client.get, NOTES_DETAIL_URL, HTTPStatus.FOUND),
            (self.client.get, NOTES_EDIT_URL, HTTPStatus.FOUND),
            (self.client.get, NOTES_SUCCESS_URL, HTTPStatus.FOUND),
            (self.client.get, NOTES_DELETE_URL, HTTPStatus.FOUND),
        )
        for client, url, expected_status in test_cases:
            with self.subTest(client=client, url=url,
                              expected_status=expected_status):
                response = client(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        for url, expected_redirect in {
            NOTES_DETAIL_URL: REDIRECT_NOTES_DETAIL_URL,
            NOTES_EDIT_URL: REDIRECT_NOTES_EDIT_URL,
            NOTES_DELETE_URL: REDIRECT_NOTES_DELETE_URL,
            NOTES_ADD_URL: REDIRECT_NOTES_ADD_URL,
            NOTES_SUCCESS_URL: REDIRECT_NOTES_SUCCESS_URL,
            NOTES_LIST_URL: REDIRECT_NOTES_LIST_URL,
        }.items():
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), expected_redirect)
