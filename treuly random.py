import requests
from bs4 import BeautifulSoup
import random
import os
import ctypes
import time
from PIL import Image
import urllib.request
from PIL import Image
import shutil
#width = 500
#height = 500

timerofupdate = 1/5


def is_image_broken(file_path: str) -> bool:
    try:
        with Image.open(file_path) as img:
            img.verify()
        return False
    except Exception as e:
        print(e)
        return True



def download_random_wallhaven_image():
    # Get the page with the latest wallpapers
    chance = random.randint(1,5)
    if chance == 1:
        url = f'https://wallhaven.cc/search?categories=010&purity=100&ratios=landscape&sorting=hot&order=desc&ai_art_filter=1&page='+str(random.randint(1,7))
    if chance == 2 or chance == 3:
        url = f'https://wallhaven.cc/search?categories=010&purity=100&ratios=landscape&sorting=random&order=desc&ai_art_filter=1&page='+str(random.randint(1,1000))
    if chance == 4 or chance == 5:
        url = f'https://wallhaven.cc/search?categories=010&purity=100&ratios=landscape&topRange=1M&sorting=toplist&order=desc&ai_art_filter=1&page='+str(random.randint(1,40))
    print(chance)
    #url = f'https://wallhaven.cc/search?categories=010&purity=100&atleast={width}x{height}&ratios=landscape&sorting=hot&order=desc&ai_art_filter=1&page='+str(random.randint(1,8))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the thumbnail links
    thumbs = soup.find_all('a', {'class': 'preview'})
    thumb_links = [thumb['href'] for thumb in thumbs]
    
    # Choose a random thumbnail link
    try:
        random_thumb_link = random.choice(thumb_links)
        print("ye haiyyyyyyyyyyyyyyyyyyy", random_thumb_link)
        
        # Get the page for the chosen thumbnail
        response = requests.get(random_thumb_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the full-size image link
        img = soup.find('img', {'id': 'wallpaper'})
        img_link = img['src']
        print("Ye hai image linkkkkkkk",img_link)
        
        # Download the image
        response = requests.get(img_link,headers={"User-Agent": "Mozilla/5.0"})
        
        # Save the image to a file
        #filename = img_link.split('/')[-1]
        filename="wallhaven.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)

        image_pathy = os.path.join(os.getcwd(), "wallhaven.jpg")

        if is_image_broken(image_pathy) == True:
            print("broken image. retrying to recover")

            

        
    except Exception as i:
        print(i)
            


def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)



    

while True:

    download_random_wallhaven_image()

    image_pathy = os.path.join(os.getcwd(), "wallhaven.jpg")

    if is_image_broken(image_pathy) == False:
        time.sleep(2)
        set_wallpaper(image_pathy)
        time.sleep(60*timerofupdate)

    else:
        print("corrupt wallpaperrrrr. fixing mistake")
        time.sleep(3)
