from collections import namedtuple
from math import sqrt
import random

from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))


def get_points(img):
    """
    Function for getting points of an image
    :param img: image obj
    :return: list of point obj
    """
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def colours(filename, n=4):
    """
    Function for getting dominating colours from image
    :param filename: str, name of file
    :param n: int, number of colours
    :return:
    """
    img = Image.open(filename)
    img.thumbnail((200, 200))

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)


def euclidean(p1, p2):
    """
    Function for calculating euclidean value
    :param p1: point obj
    :param p2: point obj
    :return: float
    """
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))


def calculate_center(points, n):
    """
    Function for calculating center
    :param points: list of point obj
    :param n: int
    :return: point obj
    """
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points, k, min_diff):
    """
    K-means function
    :param points: list of point obj
    :param k: int
    :param min_diff: int
    :return: list of clusters of an image
    """
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while True:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


# TODO add implementation
def get_tools_by_colours(colours):
    """
    Function for getting tools by analysing colours
    :param colours: list of str, colours
    :return: ObjectSet of tools
    """
    from apps.core.models import Tool

    return Tool.objects.none()
