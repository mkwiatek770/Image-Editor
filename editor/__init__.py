from PIL import Image
from config import Config
from resizeimage import resizeimage
from requests import get 
from bs4 import BeautifulSoup
import urllib.request
import os

class ImageEditor:
    
    def get_site(self):
        try:
            html = get(Config.URL)
            soup = BeautifulSoup(html.text, Config.PARSER)
            return soup
        except ConnectionError:
            return "Brak internetu!"    
    
    def make_dir(self):
        if not os.path.exists('media'):
            os.makedirs('media')

    def save_img(self, soup):
        n = 1
        size = Config.IMAGE_W, Config.IMAGE_H
        for image in soup.find_all('img'):
            try:
                urllib.request.urlretrieve(image['src'], "media/image{}.jpg".format(n))
            except ValueError:
                pass 
            else: 
                name = "media/image{}.jpg".format(n)
                i = Image.open(name)
                i = resizeimage.resize_cover(i, (size))
                i.save(name, image.format)
                print(i)
                if Config.WHITE_BLACK:
                    i.convert(mode="L").rotate(Config.ROTATE).save(name)
                else:
                    i.rotate(Config.ROTATE).save(name) 

                print(i)
                n += 1
    
    
    def run(self):
        soup = self.get_site()
        self.make_dir()
        return self.save_img(soup)    
