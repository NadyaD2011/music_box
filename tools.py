from sanitize_filename import sanitize
from bs4 import BeautifulSoup

import requests
import os


def save_img(author_path, url_img, name_img):
    img_path = f'{author_path}/images'
    os.makedirs(img_path, exist_ok=True)

    response = requests.get(url_img)
    response.raise_for_status()

    extension = os.path.splitext(url_img)[1]
    img_name = sanitize(f'{name_img}{extension}')

    with open(f'{img_path}/{img_name}', 'wb') as img:
        img.write(response.content)


def save_text_song(result_folder, song_author, url_song, song_name):
    response = requests.get(url_song)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    text_song = soup.select_one('.Lyrics__Container-sc-a49d8432-1')

    if text_song is None:
        print('Текст песни на странице не находится\n')
    else:
        text_song.select_one('.LyricsHeader__Container-sc-5e4b7146-1').decompose()
        text_song = text_song.get_text(separator="\n")

        folder_path = os.path.join(result_folder, song_author, 'lyrics')
        os.makedirs(folder_path, exist_ok=True)

        file_name = sanitize(f'{song_name}.txt')
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_song)
