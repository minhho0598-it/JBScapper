import json

class Cookies:
    def __init__(self):
        pass

    def load_cookies_from_file(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
            cookies = {cookie['name']: cookie['value'] for cookie in data['cookies']}
        return cookies