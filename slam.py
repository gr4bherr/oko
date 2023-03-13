#!/usr/bin/env python3 
import cv2
import os 
import matplotlib.pyplot as plt
import numpy as np
import glob


# kitti odometry dataset
# image_0: left camera, image_1: right camera
maindir = '/Volumes/t7/kitti/dataset/'
left_images = glob.glob(f'{maindir}sequences/00/image_0/*.png')
right_images = glob.glob(f'{maindir}sequences/00/image_1/*.png')

# generators (slower, but less memory intesive)
left_gen = (cv2.imread(img) for img in left_images)
right_gen = (cv2.imread(img) for img in right_images)

#file_path = f'{maindir}sequences/00/image_0/'
#plt.imshow(cv2.imread(file_path + left_images[0]))
#plt.show()

poses = np.genfromtxt(f'{maindir}poses/00.txt', delimiter=' ').reshape(-1, 3, 4)
#print(poses)
#print(poses.shape)

# rows: p0, p1, p2, p3, tr
calib = np.genfromtxt(f'{maindir}sequences/00/calib.txt', delimiter=' ')[:, 1:].reshape(-1, 3, 4)
print(calib)
print(calib.shape)


velodyne_files = os.listdir(f'{maindir}sequences/00/velodyne')
print(len(velodyne_files))
# columns: px, py, pz, pr
pointcloud = np.fromfile(f'{maindir}sequences/00/velodyne/{velodyne_files[0]}', dtype=np.float32).reshape(-1, 4)
print(pointcloud)
print(pointcloud.shape)

# plot pointcloud
#fig = plt.figure(figsize=(8, 8))
#ax = fig.add_subplot(111, projection='3d')
#xs = pointcloud[:, 0][::10]
#ys = pointcloud[:, 1][::10]
#zs = pointcloud[:, 2][::10]
#ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
#ax.scatter(xs, ys, zs, s=0.01)
#plt.show()




