from django.test import TestCase, Client


# Create your tests here.
class SearchViewTests(TestCase):
    def test_with_null_key(self):
        client = Client()
        key = None
        response = client.get('/search/?key=')

    def test__with_valued_key(self):
        pass
