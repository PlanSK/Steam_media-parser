from bs4 import BeautifulSoup
import requests
import os

import gsheets


def write_media_link(
    path_data: tuple, type_media: str, src_link: str, 
    media_counter: int = 0
    ) -> str:

    id = path_data[0]
    title = path_data[1]
    folder = path_data[2]
    counter = ''


    if media_counter:
        counter = str(media_counter)

    if '?' in src_link:
        src_link = src_link.split('?')[0]
    
    file_name_tail = src_link.split('.')[-1]
    image_file_name = f'{type_media}{counter}-{id}-{title}.{file_name_tail}'

    if os.path.exists(folder):
        image_file_path = os.path.join(folder, image_file_name)
    else:
        raise FileNotFoundError('Folder does not exsists.')

    if not os.path.exists(image_file_path):
        image_buffer = requests.get(url=src_link)
        with open(image_file_path, 'wb') as img_file:
            img_file.write(image_buffer.content)
    else:
        print(f'{image_file_path} exists - passed.')


    return image_file_name


if __name__ == "__main__":
    print('Esports Tatar Steam Parser (c)')

    table = '1HXP6i8m1MfofyY-nUDx8F686NME_poBrlU8nDdidYso'
    export_data = dict()
    games_list_file = 'games.list'
    games_list = []
    with open(games_list_file, 'r') as data_file:
        games_list = [int(id.strip()) for id in data_file]

    for game_id in games_list:
        url_steam = f'https://store.steampowered.com/app/{game_id}/?l=russian'
        page = requests.get(url=url_steam)
        soup = BeautifulSoup(page.text, "lxml")

        if page.status_code == 200:
            game_title = soup.find(id='appHubAppName').string
            game_folder_name = f'{game_title}-{game_id}'

            if not os.path.exists(os.path.join(os.getcwd(), 'data')):
                os.mkdir(os.path.join(os.getcwd(), 'data'))

            abs_folder_path = os.path.join(os.getcwd(), 'data', game_folder_name)
            write_data = (game_id, game_title, abs_folder_path)

            if not os.path.exists(abs_folder_path):
                os.mkdir(abs_folder_path)

            main_game_image_src = soup.find(class_='game_header_image_full')['src']
            main_game_image = write_media_link(write_data, 'main_img', main_game_image_src)

            game_icon_src = soup.find(class_='apphub_AppIcon').img['src']
            game_icon = write_media_link(write_data, 'icon', game_icon_src)

            short_description = soup.find(class_='game_description_snippet').string.strip()

            tags = [
                tag.string.strip()
                for tag in soup.find(class_='glance_tags popular_tags').find_all('a')
            ]
            genres = [
                genre.string
                for genre in soup.find(id='genresAndManufacturer').span.find_all('a')
            ]
            media_data = soup.find(id='highlight_player_area')
            mp4_files = media_data.find_all('div', 'highlight_player_item highlight_movie')
            screenshots = media_data.find_all('div', 'highlight_player_item highlight_screenshot')

            media_files_list = []

            for number, img_media in enumerate(screenshots, start=1):
                media_src = img_media.div.find('a', 'highlight_screenshot_link')['href']
                media_files_list.append(write_media_link(write_data, 'screenshot', media_src, media_counter=number))

            for number, mp4_media in enumerate(mp4_files, start=1):
                media_src = mp4_media['data-mp4-source']
                media_files_list.append(write_media_link(write_data, 'video', media_src, media_counter=number))

            export_data.update({ game_id : {
                'title': game_title,
                'icon': game_icon,
                'genres': ', '.join(genres),
                'main_img': main_game_image,
                'tags': ', '.join(tags),
                'description': short_description,
                'screenshots': ', '.join(media_files_list)
                } }
            )
        else:
            pass

gsheets.gsheets_save(table, export_data)