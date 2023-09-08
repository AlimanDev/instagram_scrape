import os
import requests

from typing import List

from scrape import InstagramParser


def get_or_create_path(profile_name):
    dir_path = f"posts/{profile_name}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Каталог {dir_path} создан успешно.")
    else:
        print(f"Каталог {dir_path} уже существует.")

    return dir_path


def images_save(images_url: List[str], save_directory: str, post_number: int):
    for photo_number, image_url in enumerate(images_url):
        filename = os.path.join(save_directory, f'post_{post_number}_photo_{photo_number + 1}.png')
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Изображение сохранено в {filename}")
        else:
            print(f"Не удалось скачать изображение. Код состояния: {response.status_code}, {response.reason}")


if __name__ == '__main__':
    f = open(f'profiles.txt', 'rb')
    profiles = f.readlines()
    f.close()
    for profile in profiles:
        profile_name = profile.decode().replace('\n', '')
        print(f'Profile name: {profile_name}')
        directory_path = get_or_create_path(profile_name)

        iterator = InstagramParser(username=profile_name)
        i_count = 1
        while True:
            try:
                data = next(iterator)
                images = data['images']
                images_save(images, directory_path, i_count)
                i_count += 1
            except Exception as e:
                print(f'Raise error message: {e}')
                break

