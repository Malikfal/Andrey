import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFilter
import os

def pil_cat():
    url = 'https://krasivosti.pro/koshki/8125-kot-smotrit-v-kameru.html'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "lxml")
    cats2 = soup.find_all(class_="highslide")

    for i in range(44):
        try:
            img = requests.get(cats2[i].get("href"))
            out = open(f"images\cats\cat{i+2}.jpg", "wb")
            out.write(img.content)
            out.close()

            img = Image.open(f"images\cats\cat{i+2}.jpg")
            img.thumbnail((64,64))
            img.save(f"images\cats\cat{i+2}.png")
        except:
            pass

def del_none():
    for i in range(44):
        try:
            os.remove(f"images\cats\cat{i+2}.jpg")
            
        except:
            pass



def func():
    img = Image.open(f"images\chel.png")
    img2 = Image.open(f"images\cats\cat1.png")
    
    mask_im = Image.new("L",img2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((5, 5, 64, 64), fill=255)
    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(2))
    
    img.paste(img2, (24, 28), mask_im_blur)
    img.save('images\cotochel.png')
    
    img.close()
    img2.close()
    mask_im.close()

func()

def normal():
    for i in range(45):
        try:
            img = Image.open(f"images\cats\cat{i+1}.png")
            width = 64
            height = 64
            resized_img = img.resize((width, height), Image.ANTIALIAS)
            resized_img.save(f"images/cats2/cat{i+1}.png")
        except:
            pass


#del_none()