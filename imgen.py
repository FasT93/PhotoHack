import numpy as np
import scipy.optimize as opt
from genetic import GeneticAlgorithm

def intersection(rect1, rect2):
    dx = min(rect1[0] + rect1[2], rect2[0] + rect2[2]) - max(rect1[0], rect2[0])
    dy = min(rect1[1] + rect1[3], rect2[1] + rect2[3]) - max(rect1[1], rect2[1])
    if (dx >= 0) and (dy >= 0):
        return dx * dy
    return 0

def intersections(rects):
    result = 0
    for i in range(len(rects) - 1):
        for j in range(i + 1, len(rects)):
            result += intersection(rects[i], rects[j])
    return result

def intersections_with_box(rects, box):
    result = 0
    for rect in rects:
        result += intersection(rect, box)
    return result

def order(rects):
    result = 0
    coeff = 0.9
    for i in range(len(rects) - 1):
        x1 = rects[i][0] + coeff * rects[i][2]
        y1 = rects[i][1] + coeff * rects[i][3]
        for j in range(i + 1, len(rects)):
            x2 = rects[j][0]
            y2 = rects[j][1]
            if y1 > y2:
                result += 10 * (y1 - y2)
            if x1 > x2:
                result += (x1 - x2) / 10
    return result




class ImageGenerator():
    def __init__(self, imgsize):
        self.imgize = imgsize
        self.space = 10
        self.func = self.fitness_test
        self.sizes = []
        self.face_rect = None

    def width(self):
        return self.imgize[0]

    def height(self):
        return self.imgize[1]

    def count(self):
        return len(self.sizes)

    def fitness(self, x):
        if len(x.shape) == 1:
            return self.func(x)
        result = np.zeros(x.shape[0])
        for i, row in enumerate(x):
            result[i] = self.func(row)
        return result

    def draw(self, sizes):
        self.sizes = [(s[0] + 2 * self.space, s[1] + 2 * self.space) for s in sizes]
        maxvals = [self.width() - s[0] - 2 * self.space for s in sizes]
        maxvals.extend([self.height() - s[1] - 2 * self.space for s in sizes])
        ga = GeneticAlgorithm()
        ga.population = 150
        ga.n_iters = 1000
        ga.mutation_prob = 0.4
        ga.dim = 2 * self.count()
        ga.mutation_factor = min(self.width(), self.height()) / 2
        ga.set_minvals(self.space)
        ga.set_maxvals(maxvals)
        _, minx = ga.minimize(self.fitness)
        return minx + self.space

    def fitness_test(self, v):
        f = 0
        x = v[np.arange(0, self.count())]
        y = v[np.arange(self.count(), 2 * self.count())]
        rects = [(x[i], y[i], self.sizes[i][0], self.sizes[i][1]) for i in range(self.count())]
        f += np.sqrt(2 * intersections(rects))
        f += np.sqrt(4 * order(rects))
        f += np.sqrt(intersections_with_box(rects, self.face_rect))
        return f

