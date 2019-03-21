import cv2
import numpy as np
from PIL import Image

# Convert PIL image to OpenCV image
def pil2cv(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Convert OpenCV image to PIL image
def cv2pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Detect face on image
def haar_detector(img):
    img_cv = pil2cv(img)
    face_detector = cv2.CascadeClassifier('resources/haarcascade_frontalface.xml')
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    return faces

# Draw frame on image
def draw_frame(img, rect):
    img_cv = pil2cv(img)
    x, y = rect[0], rect[1]
    w, h = rect[2], rect[3]
    cv2.rectangle(img_cv, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return cv2pil(img_cv)