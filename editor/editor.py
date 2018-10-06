from PIL import Image
from config import Config
from resizeimage import resizeimage
from requests import get 
from bs4 import BeautifulSoup
import urllib.request
import os
import re

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

    def img_name(self, name):
        pattern = re.compile(r"https://encrypted-tbn0.gstatic.com/images\?q=tbn:(\w+)")
        img_name = "{}.jpg".format(pattern.search(name).group(1))
        return img_name

    def save_image(self, img_name):
        size = Config.IMAGE_W, Config.IMAGE_H
        name = "media/{}".format(img_name)
        i = Image.open(name)
        i = resizeimage.resize_cover(i, (size))
        i.save(name)
        print("Saving image {}".format(img_name))
        if Config.WHITE_BLACK:
            i.convert(mode="L").rotate(Config.ROTATE).save(name)
        else:
            i.rotate(Config.ROTATE).save(name)

    def save_img(self):
        for image in self.get_site().find_all('img'):
            try:
                img_name = self.img_name(image['src'])
                print("Downloading image ...")
                urllib.request.urlretrieve(image['src'], "media/{}".format(img_name))
            except (ValueError, AttributeError):
                pass 
            else: 
                self.save_image(img_name)
    
    
    def run(self):
        soup = self.get_site()
        self.make_dir()
        return self.save_img()    
