from textdrawer import TextDrawer
from textproc import TextProcessor
from imgproc import save_images

text = '  Привет,   дружище,   ;как: 0129 дела?'

tp = TextProcessor()
words = tp.parse(text)

td = TextDrawer()
td.mode = 'cornered'
td.textcolor_mode = 'contrast'
td.backcolor_mode = 'random'
td.fontsize_mode = 'random'
td.fontsize_min = 30
td.fontsize_max = 40
td.font_mode = 'random'
td.font_folder = 'fonts'

imgs = td.draw(words)
save_images(imgs, 'output/img.png')