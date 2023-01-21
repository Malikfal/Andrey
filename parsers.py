import requests
from PIL import Image, ImageDraw, ImageFilter
from bs4 import BeautifulSoup
from random import randint

class Parsers:
    def __init__(self):
        self.bd = []
        self.now_url = 0

    # Обрезка карты
    def pil_map(self):
        img = Image.open('images/map.jpg')
        im_crop = img.crop((0, 0, 1240, 1645))
        im_crop.save('images/map2.png')

    # Парсинг карты
    def get_map(self):
        url = "https://www.rbc.ru/politics/11/01/2023/621a39ba9a79472784f029d4"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "lxml")
        map_url = soup.find(class_="smart-image__img",alt="Военная операция на Украине. Карта").get("src")

        img = requests.get(map_url)
        out = open("images\map.jpg", "wb")
        out.write(img.content)
        out.close()
        
        self.pil_map()

    # коточел
    def cotochel(self):
        url = requests.get('https://randomuser.me/api/?results=1&noinfo')
        json = url.json()
        people_img_url = (json.get('results')[0]).get('picture').get("large")

        people = requests.get(people_img_url)
        out = open("images\chel.png", "wb")
        out.write(people.content)
        out.close()

        img = Image.open(f"images\chel.png")
        img2 = Image.open(f"images\cats\cat{randint(1,44)}.png")
        
        mask_im = Image.new("L",img2.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((5, 5, 64, 64), fill=255)
        mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(2))
        
        img.paste(img2, (26, 30), mask_im_blur)
        img.save('images\cotochel.png')
        
        img.close()
        img2.close()
        mask_im.close()

    def pil_cat(self):
        url = 'https://krasivosti.pro/koshki/8125-kot-smotrit-v-kameru.html'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "lxml")
        cats2 = soup.find_all(class_="highslide")
        cats = soup.find_all(class_="highslide")[1].get('href')
        return len(cats2)

    def news(self):
        url = 'https://www.rbc.ru/short_news'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "lxml")
        news = soup.find_all(class_="item__link")
        self.bd.append(news[0].get("href"))
        for i in news[1:10]:
            if i not in self.bd:
                self.bd.append(i.get('href'))
        self.now_url = 0
        return news[0].get("href")

        #print(news)

    def next_news(self):
        try:
            self.now_url+=1
            return self.bd[self.now_url]
        except:
            return "Актуальные новости закончились"
