import unittest
import app as target
import requests


class TestApp(unittest.TestCase):

    def test_api_endpoint(self):
        url = 'https://restcountries.com/v3.1/all'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "Endpoint está fallando")

    def test_sha1_function(self):
        languages = ['PORTUGAL', 'ESPAÑOL']
        languages_sha_1 = ['459588B894012690C5F5F490757C3A54D65FD207',
                           '54AF4E8E8A54AB7ABD40EBA89EE5F920CFED8EA9']
        languages_enc_hex = target.encript_language(languages=languages)
        self.assertEqual(languages_enc_hex, languages_sha_1,
                         "SHA-1 Generator is failing")


if __name__ == '__main__':

    unittest.main()
