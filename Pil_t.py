from PIL import Image



def pil_map():
    
    img = Image.open('images/cat.jpg')
    im_rgba = img.putalpha(128)
    im_rgba.save('images/cat2.png')

