from tools import save_img, save_text_song
from dotenv import load_dotenv

import argparse
import requests
import os


def get_songs(headers, id):
    url = f'https://api.genius.com/artists/{id}/songs'

    file_path_parent = 'songs'
    os.makedirs(file_path_parent, exist_ok=True)

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    songs = response.json()['response']['songs']

    for song in songs:
        name = song['title']
        author = song['artist_names']
        url_text_song = song['relationships_index_url']
        url_img = song['header_image_url']
        release_date = song['release_date_for_display']
        print(f'Название: {name}\nАвтор: {author}\nСсылка на текст песни: {url_text_song}\nСсылка на картинку песни: {url_img}\nДата выхода: {release_date}\n')

        author_path = f'{file_path_parent}/{author}'
        os.makedirs(author_path, exist_ok=True)

        save_text_song(file_path_parent, author, url_text_song, name)
        save_img(author_path, url_img, name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='id песни', type=int)
    args = parser.parse_args()

    load_dotenv()

    client_key = os.getenv("API_KEY")
    headers = {
            'Authorization': f'Bearer {client_key}'
    }

    get_songs(headers, args.id)


if __name__ == '__main__':
    main()
