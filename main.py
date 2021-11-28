from bs4 import BeautifulSoup
import requests
import os


def write_image_link(id: int, title: str, type_img: str, folder: str, src_link: str) -> str:
    image_buffer = requests.get(url=src_link)
    
    if '?' in src_link:
        src_link = src_link.split('?')[0]
    
    file_name_tail = src_link.split('.')[-1]
    image_file_name = f'{type_img}-{id}-{title}.{file_name_tail}'
    if os.path.exists(folder):
        image_file_path = os.path.join(folder, image_file_name)
    else:
        raise FileNotFoundError('Folder does not exsists.')
    with open(image_file_path, 'wb') as img_file:
        img_file.write(image_buffer.content)

    return image_file_name


if __name__ == "__main__":
    iter_list = [621060, 427520, 570]
    print('Esports Tatar Steam Parser (c)')    

    for game_id in iter_list:
        url_steam = f'https://store.steampowered.com/app/{game_id}/?l=russian'
        page = requests.get(url=url_steam)
        soup = BeautifulSoup(page.text, "lxml")

        if page.status_code == 200:
            tags = []
            game_title = soup.find(id='appHubAppName').string
            game_folder_name = f'{game_title}-{game_id}'
            abs_folder_path = os.path.join(os.getcwd(), 'data', game_folder_name)
            if not os.path.exists(abs_folder_path):
                os.mkdir(abs_folder_path)
            main_game_image_src = soup.find(class_='game_header_image_full')['src']
            main_game_image = write_image_link(
                id=game_id,
                title=game_title,
                type_img='main_img',
                folder=abs_folder_path,
                src_link=main_game_image_src
            )

            game_icon_src = soup.find(class_='apphub_AppIcon').img['src']
            game_icon = write_image_link(
                id=game_id,
                title=game_title,
                type_img='icon',
                folder=abs_folder_path,
                src_link=game_icon_src
            )

            short_description = soup.find(class_='game_description_snippet').string.strip()

            tags = [
                tag.string.strip()
                for tag in soup.find(class_='glance_tags popular_tags').find_all('a')
            ]
            genres = [
                genre.string
                for genre in soup.find(id='genresAndManufacturer').span.find_all('a')
            ]
        else:
            raise BaseException(f'Bad request. {page.status_code}')
