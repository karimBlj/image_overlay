import numpy as np
from html2image import Html2Image
from typing import List, Tuple

Point = Tuple[int, int]

def get_closest_point_index(points : List[Point], new_point : Point):
    dist_list = []
    np_new_point = np.array(new_point)
    for point in points:
        dist = np.linalg.norm(np.array(point) - np_new_point)
        dist_list.append(dist)
    closes_point_index = np.array(dist_list).argmin()
    return closes_point_index

def sort_pts(points):
    sorted_pts = np.zeros((4, 2), dtype="float32")
    s = np.sum(points, axis=1)
    sorted_pts[0] = points[np.argmin(s)]
    sorted_pts[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    sorted_pts[1] = points[np.argmin(diff)]
    sorted_pts[3] = points[np.argmax(diff)]

    return sorted_pts

def screen_web_page(page_url : str, dest_img : str):
    hti = Html2Image(size=(1520, 880))
    hti.screenshot(url=page_url, save_as=dest_img)
