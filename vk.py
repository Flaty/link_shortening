import requests
from urllib.parse import urlparse
from environs import Env


def is_shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'v': '5.199',
        'url': url
    }

    response = requests.get('https://api.vk.com/method/utils.checkLink', headers=headers, params=params)
    response.raise_for_status()
    response_data = response.json()
    parsed_url = urlparse(url)
    return parsed_url.netloc in 'vk.cc' and 'not_banned' in response_data['response']['status']


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'v': '5.199',
        'url': url
    }

    response = requests.get('https://api.vk.com/method/utils.getShortLink', headers=headers, params=params)
    response.raise_for_status()
    response_data = response.json()
    if 'response' in response_data:
        short_link = response_data['response']['short_url']
        return print(short_link)
    else:
        raise requests.exceptions.HTTPError


def count_clicks(token, link):
    parsed_url = urlparse(link)
    link = parsed_url.path.split('/')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'v': '5.199',
        'key': link
    }
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', headers=headers, params=params)
    response.raise_for_status()
    response_data = response.json()
    if 'response' in response_data:
        stats_link = response_data['response']['stats'][0]['views']
        return print(stats_link)
    else:
        raise requests.exceptions.HTTPError


if __name__ == "__main__":
    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')

    user_input = input('Введите свою ссылку для сокращения: ')
    try:
        if is_shorten_link(vk_token, user_input):
            count_clicks(vk_token, user_input)
        else:
            shorten_link(vk_token, user_input)
    except requests.exceptions.HTTPError:
        print('Вы ввели неправильную ссылку')
