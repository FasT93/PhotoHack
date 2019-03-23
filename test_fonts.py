from imgproc import save_images
from textdrawer import TextDrawer
import os

text = 'Тест! Test? 01234:56789'

fontnames = os.listdir('fonts')

td = TextDrawer()
td.backcolor = (27, 155, 205)
td.textcolor = (255, 255, 255)
td.fontsize = 30

for font in fontnames:
    td.font = 'fonts/' + font
    img = td.draw([text])
    save_images(img, 'output/' + font[:font.find('.')] + '.png')