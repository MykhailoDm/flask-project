import unittest
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:5000/"
USER = "user"
PLAYLIST = "playlist"
MUSIC = "music"


class MyTestCase(unittest.TestCase):
    def tearDown(self):
        BASE_URL = None
        USER = None
        PLAYLIST = None
        MUSIC = None

    def test_get_user(self):
        r = requests.request("GET", BASE_URL + USER)
        self.assertEqual(r.status_code, 200)

    def test_get_playlist(self):
        r = requests.request("GET", BASE_URL + PLAYLIST)
        self.assertEqual(r.status_code, 200)

    def test_get_music(self):
        r = requests.request("GET", BASE_URL + MUSIC)
        self.assertEqual(r.status_code, 200)

    def test_post_user(self):
        r = requests.request("POST", BASE_URL + USER)
        self.assertEqual(r.status_code, 500)

    def test_post_playlist(self):
        r = requests.request("POST", BASE_URL + PLAYLIST, auth=HTTPBasicAuth("Super", "pass"))
        self.assertEqual(r.status_code, 400)

    def test_post_music(self):
        r = requests.request("POST", BASE_URL + MUSIC)
        self.assertEqual(r.status_code, 401)

    def test_put_user(self):
        r = requests.request("POST", BASE_URL + USER)
        self.assertEqual(r.status_code, 500)

    def test_put_playlist(self):
        r = requests.request("POST", BASE_URL + PLAYLIST)
        self.assertEqual(r.status_code, 401)

    def test_put_music(self):
        r = requests.request("POST", BASE_URL + MUSIC)
        self.assertEqual(r.status_code, 401)

    def test_delete_user(self):
        r = requests.request("DELETE", BASE_URL + USER + "/111111")
        self.assertEqual(r.status_code, 200)

    def test_delete_playlist(self):
        r = requests.request("DELETE", BASE_URL + PLAYLIST + "/111111")
        self.assertEqual(r.status_code, 200)

    def test_delete_music(self):
        r = requests.request("DELETE", BASE_URL + MUSIC + "/111111")
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
