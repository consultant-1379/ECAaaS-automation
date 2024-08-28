from dbhost.constants import API_ACCESS_PORT as port
from api import invoke_post_request_without_header


class Authentication:
    def __init__(self, ip, username, password):
        self.hostip = ip
        self.username = username
        self.password = password

    def generate_nexenta_auth_token(self):
        auth_url = "https://{}:{}/auth/login".format(self.hostip, port)
        req_body = {'username': self.username, 'password': self.password}

        auth_token_response = invoke_post_request_without_header(auth_url, req_body).json()
        return str(auth_token_response['token'])
