from tools import save_img, save_text_song
from dotenv import load_dotenv

import argparse
import requests
import os


def search_song(headers, search):
    url = 'https://api.genius.com/search'
    params = {
        'q': search
    }

    file_path_parent = 'songs'
    os.makedirs(file_path_parent, exist_ok=True)

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    hits = response.json()['response']['hits']

    for hit in hits:
        hit = hit['result']

        name = hit['title']
        author = hit['artist_names']
        url_text_song = hit['url']
        url_img = hit['header_image_thumbnail_url']
        release_date = hit['release_date_for_display']
        print(f'Название: {name}\nАвтор: {author}\nСсылка на текст песни: {url_text_song}\nСсылка на картинку песни: {url_img}\nДата выхода: {release_date}\n')

        author_path = f'{file_path_parent}/{author}'
        os.makedirs(author_path, exist_ok=True)

        save_text_song(file_path_parent, author, url_text_song, name)
        save_img(author_path, url_img, name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('search', help='поисковой запрос', type=str)
    args = parser.parse_args()

    load_dotenv()

    client_key = os.getenv("API_KEY")
    headers = {
            'Authorization': f'Bearer {client_key}'
    }

    search_song(headers, args.search)


if __name__ == '__main__':
    main()
