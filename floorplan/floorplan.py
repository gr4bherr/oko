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
step = int(screen_h * 0.01)

running = True
pointarr = []
black = (0,0,0)
dist = 100

# primitive collision
def nearwall(x,y):
  # i know dims are ratio 1:1, but what if they are not
  for i in range(rect_w):
    if background.get_at((x+i,y)) == black or background.get_at((x+i,y+rect_h)) == black:
      return False
  for i in range(rect_h):
    if background.get_at((x,y+i)) == black or background.get_at((x+rect_w,y+i)) == black:
      return False
  return True

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
  for angle in np.linspace(0, 2 * math.pi):
    for d in range(0, dist):
      xx = int(d * math.cos(angle)) + x
      yy = int(d * math.sin(angle)) + y
      if 0 < xx < screen_w and 0 < yy < screen_h: # in screen
        if background.get_at((xx,yy)) == black: # is wall
          if (xx,yy) not in pointarr: # no duplicates
            pointarr.append((xx,yy))
          break # break so it doesn't see through walls
  
  # draw
  points.fill("black")
  for pxl in pointarr:
    points.set_at(pxl, (255,0,0))

  # display
  screen.blit(points, (0,0))
  clock.tick(60) # 60 fps
  pygame.draw.rect(screen, (255,255,255), (x, y, rect_w, rect_h))
  pygame.display.update()
