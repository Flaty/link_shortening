import requests
from urllib.parse import urlparse
from environs import Env
env = Env()
env.read_env()


VK_TOKEN = env.str('VK_TOKEN')


def is_shorten_link(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc in 'vk.cc':
        return True
    else:
        return False


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
        return print(f'Ваша сокращенная ссылка: {short_link}')
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
        if response_data['response'].get('stats', []):
            stats_link = response_data['response']['stats'][0]['views']
            return print(f'Количество переходов по вашей ссылке: {stats_link}')
        print('Статы пока нету :(')
    else:
        raise requests.exceptions.HTTPError


if __name__ == "__main__":
    user_input = input('Введите свою ссылку для сокращения: ')
    try:
        if is_shorten_link(user_input):
            count_clicks(VK_TOKEN, user_input)
        else:
            shorten_link(VK_TOKEN, user_input)
    except requests.exceptions.HTTPError:
        print('Вы ввели неправильную ссылку')
