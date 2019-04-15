from PIL import Image
from facedetector import draw_frames, mtcnn_detector

img = Image.open('images/vlad.jpg')
faces = mtcnn_detector(img)


if len(faces) == 0:
    print('No face =(')
else:
    result = draw_frames(img, faces)
    result.show()
