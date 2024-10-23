import requests
import sys
from environs import Env
env = Env()
env.read_env()


ACCESS_TOKEN = env.str('ACCESS_TOKEN')


def is_shorten_link(url):
    if url[:14] in 'https://vk.cc/':
        print('Статистика по кликам: ', count_clicks(ACCESS_TOKEN, url))
    else:
        print('Сокращенная ссылка: ', shorten_link(ACCESS_TOKEN, url))


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'v': '5.199',
        'url': url
    }

    response = requests.get('https://api.vk.com/method/utils.getShortLink', headers=headers, params=params)

    data = response.json()
    if 'response' in data:
        return data['response']['short_url']
    else:
        raise requests.exceptions.HTTPError


def count_clicks(token, link):
    link = link[14:]
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'v': '5.199',
        'key': link
        
    }
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', headers=headers, params=params)
    data = response.json()
    if 'response' in data:
        return data['response']['stats'][0]['views']
    else:
        raise requests.exceptions.HTTPError


if __name__ == "__main__":
    user_input = input('Введите свою ссылку для сокращения: ')
    try:
        is_shorten_link(user_input)
    except requests.exceptions.HTTPError:
        print('Вы ввели неправильную ссылку')
        sys.exit()
