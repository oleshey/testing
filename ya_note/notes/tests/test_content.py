from notes.forms import NoteForm
from .conftest import (
    NOTES_LIST_URL,
    NOTES_ADD_URL,
    NOTES_EDIT_URL,
    BaseTestData
)


class TestContent(BaseTestData):

    def test_notes_list_for_author(self):
        response = self.author_client.get(NOTES_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])
        note_in_list = response.context['object_list'].get(id=self.note.id)
        self.assertEqual(note_in_list.title, self.note.title)
        self.assertEqual(note_in_list.text, self.note.text)
        self.assertEqual(note_in_list.slug, self.note.slug)
        self.assertEqual(note_in_list.author, self.note.author)

    def test_notes_list_for_reader(self):
        response = self.reader_client.get(NOTES_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        urls = (NOTES_ADD_URL, NOTES_EDIT_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
