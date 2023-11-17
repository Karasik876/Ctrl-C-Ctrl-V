import cv2
import numpy as np
# import cryptocode
import uuid


def rectangle_contour(contours):
    rect_contours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            if len(approx) == 4:
                rect_contours.append(i)
    rect_contours = sorted(rect_contours, key=cv2.contourArea, reverse=True)
    return rect_contours


def get_corner_points(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    return approx


def reorder(points):
    points = points.reshape((4, 2))
    npoints = np.zeros((4, 1, 2), np.int32)
    add = points.sum(1)
    npoints[0] = points[np.argmin(add)]
    npoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    npoints[1] = points[np.argmin(diff)]
    npoints[2] = points[np.argmax(diff)]
    return npoints


def split_boxed(img, questions, answers):
    rows = np.vsplit(img, questions)
    boxes = []
    for row in rows:
        cols = np.hsplit(row, answers)
        for box in cols:
            boxes.append(box)
    return boxes


def show_answers(img, index, grading, answers, questions, choices):
    secW = int(img.shape[1] / choices)
    secH = int(img.shape[0] / questions)
    for x in range(0, questions):
        ans = index[x]
        cX = (ans * secW) + secW // 2
        cY = (x * secH) + secH // 2

        if grading[x] >= 1:
            rep_color = (0, 255, 0)
        else:
            rep_color = (255, 0, 0)
            cv2.circle(img, (answers[x] * secW + secW // 2, x * secH + secH // 2), int(secH/2), (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (cX, cY), int(secH/2), rep_color, cv2.FILLED)
    return img


# def encrypt(text):
#     return f'{cryptocode.encrypt(text, "omr")}'
#
#
# def decrypt(value):
#     return cryptocode.decrypt(value, 'omr')
