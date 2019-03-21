import os
import collections
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from imgproc import trans_paste, luminance

# Class for drawing texts
class TextDrawer():
    def __init__(self):
        self.mode = 'default'

        self.fontsize_mode = 'fixed'
        self.fontsize = 20
        self.fontsize_min = 15
        self.fontsize_max = 25

        self.font_mode = 'fixed'
        self.font = 'arial'
        self.font_folder = None

        self.backcolor_mode = 'fixed'
        self.backcolor = (255, 255, 255)

        self.textcolor_mode = 'fixed'
        self.textcolor = (255, 0, 0)

        self.textspace_mode = 'fixed'
        self.textspace = 5
        self.textspace_min = 5
        self.textspace_max = 10

        self.cornersize_mode = 'fixed'
        self.cornersize = 20
        self.cornersize_min = 15
        self.cornersize_max = 25

    def draw(self, text):
        if not isinstance(text, collections.Iterable):
            text = [text]
        images = []
        for t in text:
            font, fontsize, backcolor, textcolor, space, cornersize = self.__get_params()
            if self.mode == 'default':
                img = self.__draw_default_text(t, font, fontsize, space, backcolor, textcolor)
            elif self.mode == 'cornered':
                img = self.__draw_cornered_text(t, font, fontsize, space, cornersize, backcolor, textcolor)
            images.append(img)
        return images

    def __get_random_font(self):
        if self.font_folder is None:
            return self.font
        else:
            fonts = os.listdir(self.font_folder)
            index = np.random.randint(0, len(fonts))
            return self.font_folder + '/' + fonts[index]

    def __get_second_bw_color(self, color):
        lum = luminance(color)
        if lum > 165:
            return (0, 0, 0)
        else:
            return (255, 255, 255)

    def __get_textcolor(self):
        if self.textcolor_mode == 'fixed':
            tcol = self.textcolor
        elif self.textcolor_mode == 'random':
            tcol = tuple(np.random.randint(0, 256, 3))
        else:
            tcol = self.textcolor
        return tcol

    def __get_params(self):
        if self.fontsize_mode == 'fixed':
            fontsize = self.fontsize
        elif self.fontsize_mode == 'random':
            fontsize = np.random.randint(self.fontsize_min, self.fontsize_max + 1)
        else:
            fontsize = self.fontsize

        if self.font_mode == 'fixed':
            font = self.font
        elif self.font_mode == 'random':
            font = self.__get_random_font()
        else:
            font = self.font

        if self.textcolor_mode == 'contrast':
            if self.backcolor_mode == 'contrast':
                bcol = tuple(np.random.randint(0, 256, 3))
            elif self.backcolor_mode == 'fixed':
                bcol = self.backcolor
            elif self.backcolor_mode == 'random':
                bcol = tuple(np.random.randint(0, 256, 3))
            else:
                bcol = self.backcolor
            tcol = self.__get_second_bw_color(bcol)
        else:
            if self.textcolor_mode == 'fixed':
                tcol = self.textcolor
            elif self.textcolor_mode == 'random':
                tcol = tuple(np.random.randint(0, 256, 3))
            else:
                tcol = self.textcolor

            if self.backcolor_mode == 'contrast':
                bcol = self.__get_second_bw_color(tcol)
            elif self.backcolor_mode == 'fixed':
                bcol = self.backcolor
            elif self.backcolor_mode == 'random':
                bcol = tuple(np.random.randint(0, 256, 3))
            else:
                bcol = self.backcolor

        if self.textspace_mode == 'fixed':
            tspace = self.textspace
        elif self.textspace_mode == 'random':
            tspace = np.random.randint(self.textspace_min, self.textspace_max + 1)
        else:
            tspace = self.textspace

        if self.cornersize_mode == 'fixed':
            cornersize = self.cornersize
        elif self.cornersize_mode == 'random':
            cornersize = np.random.randint(self.cornersize_min, self.cornersize_max + 1)
        else:
            cornersize = self.cornersize

        return font, fontsize, bcol, tcol, tspace, cornersize

    def __get_text_size(self, text, fontname, fontsize):
        font = ImageFont.truetype(fontname, fontsize)
        return font.getsize(text)

    def __draw_default_text(self, text, fontname, fontsize, space, backcolor, textcolor):
        s = self.__get_text_size(text, fontname, fontsize)
        img = Image.new('RGBA', (s[0] + 2 * space, s[1] + 2 * space), backcolor)
        font = ImageFont.truetype(fontname, fontsize)
        draw = ImageDraw.Draw(img)
        draw.text((space, space), text, textcolor, font)
        return img

    def __draw_cornered_text(self, text, fontname, fontsize, space, cornersize, backcolor, textcolor):
        inner_img = self.__draw_default_text(text, fontname, fontsize, space, backcolor, textcolor)
        s = inner_img.size
        w, h = s[0], s[1]
        corners = [(0, 0), (w + cornersize, 0), (w + cornersize, h + cornersize), (0, h + cornersize)]
        points = []
        for corner in corners:
            x = np.random.randint(corner[0], corner[0] + cornersize)
            y = np.random.randint(corner[1], corner[1] + cornersize)
            points.append((x, y))
        img = Image.new('RGBA', (w + 2 * cornersize, h + 2 * cornersize), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon(points, fill=backcolor)
        img = trans_paste(inner_img, img, box=(cornersize, cornersize))
        return img

