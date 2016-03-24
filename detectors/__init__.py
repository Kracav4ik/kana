# encoding: utf-8
from utils import Vec2d


def normalize_vec(v, aabb):
    x = aabb.x
    y = aabb.y
    w = aabb.w
    h = aabb.h
    return Vec2d((v.x - x)/w, (v.y - y)/h)


def denormalize_vec(v, aabb):
    x = aabb.x
    y = aabb.y
    w = aabb.w
    h = aabb.h
    return Vec2d(v.x*w + x, v.y*h + y)


def normalize(curve, aabb):
    """
    :type curve: tablet.Curve
    :type aabb: detectors.bbox.AABB
    """
    from tablet import Curve
    w = aabb.w
    h = aabb.h
    if not aabb or w == 0 or h == 0:
        return curve
    result = Curve()
    points = ((normalize_vec(v, aabb), p) for v, p in curve.points)
    result.from_row(((v.x, v.y, p) for v, p in points))
    return result

