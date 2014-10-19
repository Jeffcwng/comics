from django.test import TestCase
from xkcd.data.fetchcomics import get_all_comics


class UtilTestCase(TestCase):
    def test_get_all_comics(self):
        json_list = get_all_comics(403, 406)
        self.assertEqual(json_list[0]['num'], 403)
        self.assertEqual(json_list[1]['num'], 405)
