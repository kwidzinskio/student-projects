# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 11:28:34 2021

@author: kwidz
"""

import numpy as np
import cv2


def read_file(filename):
    return cv2.imread(filename)


def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return gray, gray_blur, edges


def color_quantization(img, k):
    data = np.float32(img).reshape((-1,3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result

img_path = 'XXX.jpg' # input image directory
image = read_file(img_path)
gray, gray_blur, edges = edge_mask(image, 3, 5)
reduced_colors = color_quantization(image, 17)
blurred = cv2.bilateralFilter(reduced_colors, d=7, sigmaColor=150, sigmaSpace=150)
cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)



cv2.imshow('original', image)
cv2.imshow('grey', gray)
cv2.imshow('grey_blur', gray_blur)
cv2.imshow('edges', edges)
cv2.imshow('reduced_colors', reduced_colors)
cv2.imshow('blurred', blurred)
cv2.imshow('cartoon', cartoon)

cv2.waitKey(0)
cv2.destroyAllWindows()
