import os
import json
import time

from dotenv import load_dotenv
from utils.cookies import Cookies
from utils.request import GraphQLClient

load_dotenv()

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


    def upwork_scraper(self):
        url = os.getenv('UPWORK_URL')
        cookies = self.cookiesFactory.load_cookies_from_file('assets/cookies/upwork.json')

        with open('assets/query/upwork', 'r') as file:
            query = file.read()
        with open('assets/headers/upwork.json', 'r') as file:
            headers = json.load(file)

        API_KEY = os.getenv('UPWORK_API_KEY')
        if API_KEY:
            headers['authorization'] = f'bearer {API_KEY}'
        else:
            raise ValueError('API_KEY environment variable is required')

        client = GraphQLClient(url, cookies, headers)
        try:
            current_timestamp = int(time.time() * 1000)
            data, status_code = client.execute_query(query, variables={'limit': 10, 'toTime': current_timestamp})
            return {
                'statusCode': status_code,
                'body': json.dumps(data)
            }
        except Exception as e:
            raise RuntimeError('Cannot load new jobs from Upwork because of: ' + str(e))
        