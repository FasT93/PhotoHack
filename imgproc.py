from PIL import Image
import collections

# Resize image to max size
def resize(img, maxsize):
    w1, h1 = img.size
    if w1 >= h1:
        w2 = maxsize
        h2 = int(round(h1 * maxsize / w1))
    else:
        w2 = int(round(w1 * maxsize / h1))
        h2 = maxsize
    return img.resize((w2, h2), Image.ANTIALIAS)

# Paste transparent image
def trans_paste(fg_img, bg_img, alpha=1.0, box=(0, 0)):
    fg_img_trans = Image.new('RGBA', fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans, fg_img, alpha)
    bg_img.paste(fg_img_trans, box, fg_img_trans)
    return bg_img

# Get color luminance
def luminance(color):
    return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

# Save images
def save_images(images, path):
    if not isinstance(images, collections.Iterable):
        images.save(path)
    else:
        if len(images) == 1:
            images[0].save(path)
        else:
            for i, img in enumerate(images):
                index = path.find('.')
                name = path[:index] + str(i + 1) + path[index:]
                img.save(name)