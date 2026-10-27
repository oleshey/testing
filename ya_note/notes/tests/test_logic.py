# notes/tests/test_logic.py
from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .conftest import (
    NOTES_ADD_URL,
    NOTES_EDIT_URL,
    NOTES_DELETE_URL,
    NOTES_SUCCESS_URL,
    REDIRECT_NOTES_ADD_URL,
    BaseTestData
)


class TestNote(BaseTestData):
    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        created_note = Note.objects.first()
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.slug, self.form_data['slug'])
        self.assertEqual(created_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(
            NOTES_ADD_URL, data=self.form_data
        )
        self.assertRedirects(response, REDIRECT_NOTES_ADD_URL)
        self.assertEqual(Note.objects.count(), 0)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        expected_slug = slugify(self.form_data['title'])
        new_note = Note.objects.first()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.author)

    def test_not_unique_slug(self):
        notes_before = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertFormError(
            form=response.context['form'],
            field='slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_author_can_edit_note(self):
        response = self.author_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.slug, self.form_data['slug'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_reader_user_cant_edit_note(self):
        response = self.reader_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        initial_count = Note.objects.count()
        response = self.author_client.post(NOTES_DELETE_URL)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        final_count = Note.objects.count()
        self.assertEqual(final_count, initial_count - 1)
        self.assertFalse(Note.objects.filter(slug=self.note.slug).exists())

    def test_reader_user_cant_delete_note(self):
        initial_count = Note.objects.count()
        response = self.reader_client.post(NOTES_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        final_count = Note.objects.count()
        self.assertEqual(final_count, initial_count)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.title, self.note.title)
        self.assertEqual(updated_note.text, self.note.text)
        self.assertEqual(updated_note.slug, self.note.slug)
        self.assertEqual(updated_note.author, self.note.author)
