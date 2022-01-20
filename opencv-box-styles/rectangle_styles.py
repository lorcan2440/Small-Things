import cv2
import numpy as np


def draw_dotted_line(img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple,
        thickness: int, spacing: int, lineType=cv2.LINE_8):

    dist = np.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])
    pts = np.linspace(pt1, pt2, int(dist / spacing))

    for p in pts:
        x, y = int(p[0]), int(p[1])
        cv2.circle(img, (x, y), thickness, color, -1, lineType)


def draw_dashed_line(img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple,
        thickness: int, spacing: int, lineType=cv2.LINE_8):

    dist = np.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])
    pts = np.linspace(pt1, pt2, int(dist / spacing))

    for i, p in enumerate(pts):
        if i % 2 == 1:
            x1, y1 = int(pts[i-1][0]), int(pts[i-1][1])
            x2, y2 = int(p[0]), int(p[1])
            cv2.line(img, (x1, y1), (x2, y2), color, thickness, lineType)


def draw_dashdot_line(img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple,
        thickness: int, spacing: int, lineType=cv2.LINE_8):

    dist = np.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])
    pts = np.linspace(pt1, pt2, int(dist / spacing))

    for i, p in enumerate(pts[1:], start=1):
        x1, y1 = int(pts[i-1][0]), int(pts[i-1][1])
        x2, y2 = int(p[0]), int(p[1])
        cv2.circle(img, (x1, y1), thickness, color, -1, lineType)
        cv2.line(img, (int(0.75 * x1 + 0.25 * x2), int(0.75 * y1 + 0.25 * y2)),
            (int(0.25 * x1 + 0.75 * x2), int(0.25 * y1 + 0.75 * y2)), color, thickness, lineType)


def draw_dotted_rectangle(img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple,
        thickness: int, spacing: int, lineType=cv2.LINE_8):

    draw_dotted_line(img, pt1, (pt2[0], pt1[1]), color, thickness, spacing, lineType)
    draw_dotted_line(img, (pt2[0], pt1[1]), pt2, color, thickness, spacing, lineType)
    draw_dotted_line(img, pt2, (pt1[0], pt2[1]), color, thickness, spacing, lineType)
    draw_dotted_line(img, (pt1[0], pt2[1]), pt1, color, thickness, spacing, lineType)


def draw_dashed_rectangle(img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple,
        thickness: int, spacing: int, lineType=cv2.LINE_8):

    draw_dashed_line(img, pt1, (pt2[0], pt1[1]), color, thickness, spacing, lineType)
    draw_dashed_line(img, (pt2[0], pt1[1]), pt2, color, thickness, spacing, lineType)
    draw_dashed_line(img, pt2, (pt1[0], pt2[1]), color, thickness, spacing, lineType)
    draw_dashed_line(img, (pt1[0], pt2[1]), pt1, color, thickness, spacing, lineType)


def draw_dashdot_rectangle(img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple,
        thickness: int, spacing: int, lineType=cv2.LINE_8):

    draw_dashdot_line(img, pt1, (pt2[0], pt1[1]), color, thickness, spacing, lineType)
    draw_dashdot_line(img, (pt2[0], pt1[1]), pt2, color, thickness, spacing, lineType)
    draw_dashdot_line(img, pt2, (pt1[0], pt2[1]), color, thickness, spacing, lineType)
    draw_dashdot_line(img, (pt1[0], pt2[1]), pt1, color, thickness, spacing, lineType)



def draw_corner_rectangle(img: np.ndarray, pt1: tuple, pt2: tuple,
        corner_color: tuple, edge_color: tuple, corner_length: int,
        corner_thickness: int = 3, edge_thickness: int = 1,
        centre_cross: bool = True, lineType=cv2.LINE_8):

    e_args = [edge_color, edge_thickness, lineType]
    c_args = [corner_color, corner_thickness, lineType]

    # edges
    cv2.line(img, (pt1[0] + corner_length, pt1[1]), (pt2[0] - corner_length, pt1[1]), *e_args)
    cv2.line(img, (pt2[0], pt1[1] + corner_length), (pt2[0], pt2[1] - corner_length), *e_args)
    cv2.line(img, (pt1[0], pt1[1] + corner_length), (pt1[0], pt2[1] - corner_length), *e_args)
    cv2.line(img, (pt1[0] + corner_length, pt2[1]), (pt2[0] - corner_length, pt2[1]), *e_args)
    # corners
    cv2.line(img, pt1, (pt1[0] + corner_length, pt1[1]), *c_args)
    cv2.line(img, pt1, (pt1[0], pt1[1] + corner_length), *c_args)
    cv2.line(img, (pt2[0], pt1[1]), (pt2[0] - corner_length, pt1[1]), *c_args)
    cv2.line(img, (pt2[0], pt1[1]), (pt2[0], pt1[1] + corner_length), *c_args)
    cv2.line(img, (pt1[0], pt2[1]), (pt1[0] + corner_length, pt2[1]), *c_args)
    cv2.line(img, (pt1[0], pt2[1]), (pt1[0], pt2[1] - corner_length), *c_args)
    cv2.line(img, pt2, (pt2[0] - corner_length, pt2[1]), *c_args)
    cv2.line(img, pt2, (pt2[0], pt2[1] - corner_length), *c_args)

    if centre_cross:
        cx, cy = int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2)
        cv2.line(img, (cx - corner_length, cy), (cx + corner_length, cy), *e_args)
        cv2.line(img, (cx, cy - corner_length), (cx, cy + corner_length), *e_args)


im = np.zeros((800, 800, 3), dtype='uint8')

draw_dotted_rectangle(im, (100, 100), (300, 300), (120, 90, 200), 2, 20)
draw_dashed_rectangle(im, (400, 100), (700, 300), (10, 100, 255), 2, 20)
draw_dashdot_rectangle(im, (100, 350), (350, 550), (255, 200, 100), 2, 40)
draw_corner_rectangle(im, (450, 350), (600, 500), (160, 180, 80), (80, 90, 40), 30)

cv2.imshow('im', im)
cv2.waitKey()
