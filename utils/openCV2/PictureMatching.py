# -*- coding: utf-8 -*-

import numpy
from cv2 import cv2


class Image:
    def __init__(self, image):
        self.image = cv2.imread(image, cv2.IMREAD_UNCHANGED)

    @property
    def width(self):
        return self.image.shape[1]

    @property
    def height(self):
        return self.image.shape[0]


class MatchImg(object):
    def __init__(self, source, template, threshod=0.95):
        """
        匹配一个图片，是否是另一个图片的局部图。source是大图，template是小图。即判断小图是否是大图的一部分。
        :param source:
        :param template:
        :param threshod: 匹配程度，值越大，匹配程度要求就越高，最好不要太小
        """
        self.source_img = source
        self.template_img = template
        self.threshod = threshod

    def set_confidence(self, confidence):
        self.threshod = confidence

    def match_template(self, method=cv2.TM_CCOEFF_NORMED):
        """
        返回小图左上角的点，在大图中的坐标。
        :param method:
        :return: list[tuple(x,y),...]
        """
        try:
            result = cv2.matchTemplate(self.source_img.image, self.template_img.image, method)
            locations = numpy.where(result >= self.threshod)
            res = list(zip(locations[1], locations[0]))  # 返回的是匹配到的template左上角那个坐标点在image中的位置，可能有多个值
            return res
        except cv2.error as e:
            print(e)

    def get_template_position(self):
        """
        获取小图在大图中，左上角和右下角的坐标
        :return: List[list[x,y,x,y],...]
        """
        res = self.match_template()
        new_pos = []
        for r in res:
            r = list(r)
            r.append(r[0] + self.template_img.width)
            r.append(r[1] + self.template_img.height)
            new_pos.append(r)
        return new_pos

    def get_img_center(self):
        """
        获取大图中，每个小图中心点所在的坐标
        :return:
        """
        pos = self.match_template()
        points = []
        for p in pos:
            x, y = p[0] + int(self.template_img.width / 2), p[1] + int(self.template_img.height / 2)
            points.append((x, y))
        return points


def load_image_file(path):
    path = path
    image = Image(path)
    return image


if __name__ == "__main__":
    img1 = load_image_file(r'E:\PyAutoProject\img\img.png')
    img2 = load_image_file(r'E:\PyAutoProject\img\img.png')

    process = MatchImg(img1, img2, 0.96)
    points = process.get_img_center()
    print(points)
