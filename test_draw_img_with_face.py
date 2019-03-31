from textdrawer import TextDrawer
from textproc import TextProcessor
from imgen import ImageGenerator
import facedetector as fd
from imgproc import join_imgs, to_transparence, resize
from PIL import Image
import numpy as np

# text = 'Это тестовый текст для того чтобы протестировать!'
text = 'Цветочки для танцев'

img = Image.open('images/flowers.jpg')
img = to_transparence(img, 0.2)
img = resize(img, 500)

res = fd.haar_detector(img)
if len(res) == 0:
    print('No face =(')
    quit()
face = res[0]

tp = TextProcessor()
words = tp.parse(text)

td = TextDrawer()
td.mode = 'cornered'
td.textcolor_mode = 'contrast'
td.backcolor_mode = 'random'
td.fontsize_mode = 'random'
td.fontsize_min = 20
td.fontsize_max = 25
td.font_mode = 'random'
td.font_folder = 'fonts'
imtexts = td.draw(words)

sizes = [im.size for im in imtexts]
ig = ImageGenerator(img.size)
ig.face_rect = face
res = ig.draw(sizes)
x = res[np.arange(0, len(res) // 2)]
y = res[np.arange(len(res) // 2, len(res))]
final_img = join_imgs(img, imtexts, list(zip(x, y)))
final_img.show()