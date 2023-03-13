#!/usr/bin/env python3 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

# kitti odometry dataset
maindir = '/Volumes/t7/kitti/dataset/'
# 0: left, 1: right
images0 = glob.glob(f'{maindir}sequences/00/image_0/*.png')
images1 = glob.glob(f'{maindir}sequences/00/image_1/*.png')
# lidar data
velodyne_binaries = glob.glob(f'{maindir}sequences/00/velodyne/*.bin')

# generators (slower, but less memory intesive)
gen0 = (cv2.imread(img) for img in images0)
gen1 = (cv2.imread(img) for img in images1)
# columns: px, py, pz, pr
point_gen = (np.fromfile(velodyne, dtype=np.float32).reshape(-1, 4) for velodyne in velodyne_binaries)

poses = np.genfromtxt(f'{maindir}poses/00.txt', delimiter=' ').reshape(-1, 3, 4)
# rows: p0, p1, p2, p3, tr
calib = np.genfromtxt(f'{maindir}sequences/00/calib.txt', delimiter=' ')[:, 1:].reshape(-1, 3, 4)

# plot pointcloud
def plot3dpoints(pointcloud):
  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_subplot(111, projection='3d')
  xs = pointcloud[:, 0][::10]
  ys = pointcloud[:, 1][::10]
  zs = pointcloud[:, 2][::10]
  ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
  ax.scatter(xs, ys, zs, s=0.01)
#plot3dpoints(next(point_gen))
#plt.show()


# disparity map for left camera
stereo = cv2.StereoSGBM_create(numDisparities = 6 * 16, blockSize = 11, 
                      P1 = 8 * 1 * 11 ** 2, P2 = 32 * 1 * 11 ** 2,
                      mode = cv2.STEREO_SGBM_MODE_SGBM_3WAY)
#stereo = cv2.StereoBM_create(numDisparities=6*16, blockSize=11)
disparities0 = stereo.compute(next(gen0), next(gen1)).astype(np.float32) / 16
disparities0[disparities0 <= 0] = 0.1 # remove negative and zero values
plt.imshow(disparities0)

# camera matrix, rotation matrix, translation vector
k0, r0, t0 = cv2.decomposeProjectionMatrix(calib[0])[:3] # p0
t0 = (t0 / t0[3])[:3]
k1, r1, t1 = cv2.decomposeProjectionMatrix(calib[1])[:3] # p0
t1 = (t1 / t1[3])[:3]

# focal lenght (pxl) * baseline (m) / disparity (pxl)
depthmap = k0[0][0] * (t1[0] - t0[0]) / disparities0

for maskval, pixel in enumerate(depthmap[0]):
  if pixel < depthmap.max(): break

# mask image, where left and right don't overlap
mask = np.zeros_like(depthmap)
cv2.rectangle(mask, (maskval, 0), (depthmap.shape[1], depthmap.shape[0]), (255), thickness=-1)

#plt.figure(figsize=(11,7))
#plt.imshow(depthmap)
#plt.hist(depthmap.flatten())

print(next(point_gen).shape)




plt.show()

