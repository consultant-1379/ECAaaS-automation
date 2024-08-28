import requests


def invoke_post_request_without_header(url, body, params=None):
    response = requests.post(url, data=body, verify=False)
    return response


def invoke_get_request(url, header, params=None):
    response = requests.get(url, headers=header, verify=False)
    return response

