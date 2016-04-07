# -*- coding: utf-8 -*-

import operator
import math


def dot_product(v1, v2):
    return sum(map(operator.mul, v1, v2))


def vector_cos(v1, v2):
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    return prod / (len1 * len2)


def dict_top_by_value(dictionary, top=0):
    if top <= 0 or top > len(dictionary):
        top = len(dictionary)
    return [w for idx, w in enumerate(sorted(dictionary, key=dictionary.get, reverse=True)) if idx < top]
