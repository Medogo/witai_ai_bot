import requests

WIT_AI_TOKEN = 'RDDH2ABXD6H7BYTFNEVNVTAMT6XJIAYD'

def send_to_wit(text):
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    response = requests.get(f'https://api.wit.ai/message?v=20230414&q={text}', headers=headers)
    return response.json()



