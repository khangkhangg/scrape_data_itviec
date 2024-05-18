import requests
from bs4 import BeautifulSoup
from credentials import username, password
from utils.constants import base_url

def get_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }
    return headers

def login(session):
    login_url = f'{base_url}/sign_in'
    headers = get_headers()
    
    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    token = soup.find('input', {'name': 'authenticity_token'})['value']
    
    payload = {
        'utf8': '✓',
        'authenticity_token': token,
        'user[email]': username,
        'user[password]': password,
        'commit': 'Sign in'
    }
    
    response = session.post(login_url, data=payload, headers=headers)
    
    if "https://itviec.com" in response.url or 'sign-in-user-avatar' in response.text:
        print("Login successful!")
    else:
        print("Login failed!")
