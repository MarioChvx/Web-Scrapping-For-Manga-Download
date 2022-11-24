import requests
from bs4 import BeautifulSoup
import re

def get_chapters_urls(start_chapter_url:str, num_chapters:int):
    """ Generates a list of urls
    EXAMPLE URL: 'https://dorohedoro.online/manga/dorohedoro-chapter-[1]/'
    """
    chapters_urls = list()
    start_num = re.search('(?<=\[)(.*?)(?=\])', start_chapter_url).group(0)
    start_num = int(start_num)
    for i in range(num_chapters):
        chapter_num = start_num + i
        chapter_url = re.sub("\[[^]]*\]", lambda x: str(start_num + i), start_chapter_url)
        chapters_urls.append((chapter_num, chapter_url))
    return chapters_urls

def soup_page(url:str):
    """ Generates a soup form a url """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_img_urls(soup:BeautifulSoup):
    """ Generates a list of strings with the URL's of the images """
    images = soup.find_all('img')
    images_urls = [image['src'] for image in images]
    return images_urls

def download_images(images_links:list):
    """ Download the images for each url in the list """
    for i, link in enumerate(images_links):
        if (link.startswith("https://")):
            with open(f'{i:02}.png','wb') as f:
                im = requests.get(link)
                f.write(im.content)