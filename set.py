import requests

def fumcz21() :
    return 5

def send_message():
    url = "https://api.telegram.org/bot6230258464:AAGamefm4mQv1BQZ0uv25Qw4PkpM7ykp614/setWebhook"
    data = {"url": "https://e1c7-46-53-248-186.eu.ngrok.io"}
    response = requests.post(url, data=data)
    return response.json()

print(send_message())

