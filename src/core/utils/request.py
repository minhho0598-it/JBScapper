import pycurl
from io import BytesIO
import json
import certifi

class GraphQLClient:
    def __init__(self, url, cookies=None, headers=None):
        self.url = url
        self.headers = headers if headers else {}
        self.cookies = cookies

    def execute_query(self, query, variables=None):
        data = {'query': query}
        if variables:
            data['variables'] = variables

        headers = [f"{key}: {value}" for key, value in self.headers.items()]
        headers.append("Content-Type: application/json") # ensure Content-Type is set
        
        if cookies:= self.cookies:
          cookie_string = "; ".join([f"{key}={value}" for key, value in cookies.items()])
          
        else:
            cookie_string=""

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, json.dumps(data))
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        
        c.setopt(c.CAINFO, certifi.where())
        
        if cookie_string:
            c.setopt(c.COOKIE, cookie_string)
        
        try:
            c.perform()
            status_code = c.getinfo(pycurl.HTTP_CODE)
            response_body = buffer.getvalue().decode('utf-8')
            response_data = json.loads(response_body)
        except pycurl.error as e:
            print(f"Pycurl error: {e}")
            return None, 500 #or any other appropriate error code
        finally:
            c.close()

        return response_data, status_code