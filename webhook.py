import requests


def setwebhook(token, web_url):
    telegram_url = f'https://api.telegram.org/bot{token}/setWebhook'
    params = {'url': web_url}
    requests.get(telegram_url, json=params).json()


def deletewebhook(token):
    telegram_url = f'https://api.telegram.org/bot{token}/deleteWebhook'
    requests.get(telegram_url).json()


# setwebhook(TOKEN, WEB_URL)
# deletewebhook(TOKEN)
