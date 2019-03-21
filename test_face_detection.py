from PIL import Image
import facedetector as fd
import imgproc as imp

img = Image.open('images/vlad.jpg')

img = imp.resize(img, 500)
print(img.size)

res = fd.haar_detector(img)
if len(res) == 0:
    print('No face =(')
else:
    img_new = fd.draw_frame(img, res[0])
    img_new.show()


