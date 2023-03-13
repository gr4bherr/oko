#!/usr/bin/env python3
import cv2 
import numpy as np
from matplotlib import pyplot as plt

def make_coordiantes(image, line_parameters):
  slope, intercept = line_parameters
  y1 = image.shape[0]
  y2 = int(y1*(3/5))
  x1 = int((y1 - intercept) / slope)
  x2 = int((y2 - intercept) / slope)
  return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
  left_fit = []
  right_fit = []
  for line in lines:
    x1, y1, x2, y2 = line.reshape(4)
    parameters = np.polyfit((x1,x2), (y1,y2), 1)
    slope = parameters[0]
    intercept = parameters[1]
    if slope < 0:
      left_fit.append((slope, intercept))
    else:
      right_fit.append((slope, intercept))
  if left_fit:
    left_fit_average = np.average(left_fit, axis=0)
    left_line = make_coordiantes(image, left_fit_average)
  else:
    left_line = np.array([0, 0, 0, 0])
  if right_fit:
    right_fit_average = np.average(right_fit, axis=0)
    right_line = make_coordiantes(image, right_fit_average)
  else:
    right_line = np.array([0, 0, 0, 0])
  return np.array([left_line, right_line])

def region_of_interes(image):
  height = image.shape[0]
  polygons = np.array([[(200, height), (1100, height), (600, 250)]]) # one polygon
  mask = np.zeros_like(image)
  cv2.fillPoly(mask, polygons, 255)
  masked_image = cv2.bitwise_and(image, mask)
  return masked_image

def draw_lines(image, lines):
  line_image = np.zeros_like(image)
  if lines is not None:
    for x1, y1, x2, y2 in lines:
      cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 5)
  return line_image

def process_frame(frame):
  #frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
  gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  blur_image = cv2.GaussianBlur(gray_image,(5,5),0)
  canny_image = cv2.Canny(blur_image, 50, 100)

  cropped_image = region_of_interes(canny_image)

  lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
  averaged_lines = average_slope_intercept(frame, lines)
  line_image = draw_lines(frame, averaged_lines)
  combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)


  cv2.imshow('frame', combo_image)

  if cv2.waitKey(1) == ord('q'):
    cv2.destroyAllWindows()
    exit()
  #plt.imshow(canny)
  #plt.show()
  #exit()



if __name__ == '__main__':
  name = 'test2.mp4'
  cap = cv2.VideoCapture(name)
  framecnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  print(f'{name}')
  print(f'  resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}')
  print(f'  duration: {int(framecnt/fps)}s')
  print(f'  fps: {fps}')
  print(f'  framecount: {framecnt}')

  i = 0
  while True:
    print(f"frame {i}/{framecnt}")
    ret, frame = cap.read()

    if ret:
      process_frame(frame)
      i += 1
    else:
      break