import json
import time
import configparser
import os

from pathlib import Path
from utils.cookies import Cookies
from utils.request import GraphQLClient

class Scraper:
    """
    A versatile web scraper class for extracting data from web pages.
    """

    def __init__(self, url=None, headers=None):
        """
        Initializes the Scraper object.

        Args:
            url (str, optional): The URL of the web page to scrape. Defaults to None.
            headers (dict, optional): Custom headers to use for the HTTP request. Defaults to None.
        """
        self.url = url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.soup = None
        self.response = None
        self.cookiesFactory = Cookies()

        # Loading config setting
        config = configparser.ConfigParser()
        # Use pathlib:
        config_file_path = Path(__file__).parent.parent / 'config' / 'appsettings.ini'
        config.read(config_file_path)
        
        self.upwork_url = config['API']['UPWORK_URL']
        self.upwork_api_key = config['API']['UPWORK_API_KEY']


    def upwork_scraper(self):
        cookies = self.cookiesFactory.load_cookies_from_file('assets/cookies/upwork.json')

        with open('assets/query/upwork', 'r') as file:
            query = file.read()
        with open('assets/headers/upwork.json', 'r') as file:
            headers = json.load(file)

        if self.upwork_api_key:
            headers['authorization'] = f'bearer {self.upwork_api_key}'
        else:
            raise ValueError('API_KEY environment variable is required')

        client = GraphQLClient(self.upwork_url, cookies, headers)
        try:
            current_timestamp = int(time.time() * 1000)
            data, status_code = client.execute_query(query, variables={'limit': 10, 'toTime': current_timestamp})
            return {
                'statusCode': status_code,
                'body': json.dumps(data)
            }
        except Exception as e:
            raise RuntimeError('Cannot load new jobs from Upwork because of: ' + str(e))
        