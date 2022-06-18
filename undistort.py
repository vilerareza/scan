#import argparse
import os
import cv2 as cv
import numpy as np
import pickle

imgDir = "img_raw"
outDir = "img_corrected"
# Argument handler
#parser = argparse.ArgumentParser()
#parser.add_argument('dir', type = str, default = '')

#args = parser.parse_args()

# Loading calibration data
try:
    camera_cal = pickle.load(open('camera_cal.p',"rb"))
    mtx = camera_cal["mtx"]
    dist = camera_cal["dist"]
    new_mtx = camera_cal["new_mtx"]
    roi = camera_cal["roi"]
except:
    print ('Calibration data does not exist')

try:
    imageFiles = os.listdir(imgDir)
    if len(imageFiles) > 0:
        for imageFile in imageFiles:
            filePath = os.path.join(imgDir, imageFile)
            img = cv.imread(filePath)
            # Undistort image with camera calibration data
            undst_image = cv.undistort(img, mtx, dist, None, new_mtx)
            # h, w = img.shape[:2]
            #mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, new_mtx, (w,h), 5)
            # undst_image = cv.remap(img, mapx, mapy, cv.INTER_NEAREST)
            # x, y, w, h = roi
            # undst_image = undst_image[y:y+h, x:x+w]
            cv.imwrite(f'{outDir}/{imageFile}',undst_image)
    else:
        print ('Source image does not exist')
except:
    print ('Source directory not found')
