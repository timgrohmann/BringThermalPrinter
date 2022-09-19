import requests
from FileHelper import FileHelper
import jwt
import time
import secret
import urllib.parse

class BringAPI():
    BASE_URL = 'https://api.getbring.com/rest/v2/'

    def __init__(self, email, password):
        self._auth = self._authenticate(email, password)
        self._uuid = self._auth['uuid']

        self._lists = []

    def _authenticate(self, email, password):
        loaded_auth = FileHelper.load_file('auth')
        if loaded_auth is not None:
            token = jwt.decode(loaded_auth["access_token"], algorithms="HS512", options={"verify_signature": False})
            if email == token["sub"] and token["exp"] > time.time():
                print("Using saved access-token")
                return loaded_auth
            else:
                print("Saved token is invalid or expired", token)

        content = {
            'email': email,
            'password': password
        }
        auth = requests.post(
            BringAPI.BASE_URL + 'bringauth', content).json()
        print(auth)
        FileHelper.save_file("auth", auth)
        return auth

    def _get_json(self, url_path, auth=True):
        url = BringAPI.BASE_URL + "/".join(url_path)
        headers = None
        if auth:
            if self._auth is None:
                raise RuntimeError(
                    'Tried to do API call before authenticating.')
            headers = {
                'Authorization': "Bearer " + self._auth['access_token'],
                'X-BRING-API-KEY': 'cof4Nc6D8saplXjE3h3HXqHH8m7VU2i1Gs0g85Sp'
            }
        return requests.get(url, headers=headers).json()

    def get_lists(self):
        if len(self._lists) > 0:
            return self._lists
        self._lists = self._get_json(
            ("bringusers", self._uuid, "lists"))["lists"]
        return self._lists

    def _list_name_to_uuid(self, name):
        chosen_list = next((l for l in self.get_lists()
                           if l['name'] == name), None)
        if chosen_list is None:
            raise RuntimeError(f"No list named {name}")
        return chosen_list["listUuid"]

    def get_list(self, name):
        return self._get_json(("bringlists", self._list_name_to_uuid(name)))["purchase"]

    def get_list_details(self, name):
        return self._get_json(("bringlists", self._list_name_to_uuid(name), "details"))

    def get_articles_locale(self):
        return FileHelper.load_or_lamda("locale-articles", requests.get('https://web.getbring.com/locale/articles.de-DE.json').json)

    def get_catalog_locale(self):
        return FileHelper.load_or_lamda("locale-catalog", requests.get('https://web.getbring.com/locale/catalog.de-DE.json').json)


if __name__ == "__main__":
    api = BringAPI(secret.USERNAME, secret.PASSWORD)
    print(api.get_articles_locale())
