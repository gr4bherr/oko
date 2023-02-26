#!/usr/bin/env python3
import sys
import pygame
import math
import numpy as np

print("\nto move, press wasd")

# init
pygame.init()
background = pygame.image.load("map.jpg")
screen_w, screen_h = background.get_size()
screen = pygame.display.set_mode((screen_w, screen_h))
points = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

# rect
x, y = 0, 0
rect_w, rect_h = 20, 20
step = 5

pointarr = []

# primitive collision
def nearwall(x,y):
  white = (255,255,255,255)
  # i know dims are ratio 1:1, but what if they are not
  for i in range(rect_w):
    if background.get_at((x+i,y)) == white or background.get_at((x+i,y+rect_h)) == white:
      return False
  for i in range(rect_h):
    if background.get_at((x,y+i)) == white or background.get_at((x+rect_w,y+i)) == white:
      return False
  return True

running = True
while running:
  pygame.time.delay(10)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # input control
  keys = pygame.key.get_pressed()
  if keys[pygame.K_a] and x-step > 0 and nearwall(x-step, y):
    x -= step
  if keys[pygame.K_d] and x+step < screen_w - rect_w and nearwall(x+step, y):
    x += step
  if keys[pygame.K_w] and y-step > 0 and nearwall(x, y-step):
    y -= step
  if keys[pygame.K_s] and y+step < screen_h - rect_h and nearwall(x,y+step):
    y += step
  #print(f"x:{x}, y:{y}")

  # lidar
  dist = 100
  for angle in np.linspace(0, 2 * math.pi):
    for d in (0, dist, 5):
      xx = int(dist * math.cos(angle)) + x
      yy = int(dist * math.sin(angle)) + y
      if 0 < xx < screen_w and 0 < yy < screen_h:
        if background.get_at((xx,yy)) == (255,255,255,255):
          pointarr.append((xx,yy))
  
  # draw
  points.fill("black")
  for pxl in pointarr:
    points.set_at(pxl, (255,0,0))

  # display
  screen.blit(points, (0,0))
  clock.tick(60) # 60 fps
  pygame.draw.rect(screen, (255,255,255), (x, y, rect_w, rect_h))
  pygame.display.update()
