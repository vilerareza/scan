import cv2 as cv
import numpy as np
import pickle
import subprocess
import time

fileName = 'capture_undistorted.png'
imgDir = "img_raw"
outDir = "img_corrected"

def capture(outDir, fileName, mtx, dist):
    t1 = time.time()
    subprocess.run(['libcamera-still', '--denoise', 'off', '--shutter', '70000', '--gain', '0', '--awb', 'cloudy', '--immediate', '--rawfull', '-e', 'png', '-o', f'{outDir}/{fileName}'])
    t2 = time.time()
    print (f'Timelapse: {t2-t1}')
    try:
        img = cv.imread(f'{outDir}/{fileName}')
        # Undistort image with camera calibration data
        undst_image = cv.undistort(img, mtx, dist, None, mtx)
        cv.imwrite(f'{outDir}/{fileName}',undst_image)
    except:
        print ('Image not found')
try:
    # Loading calibration data
    camera_cal = pickle.load(open('../camera_cal.p',"rb"))
    #camera_cal = pickle.load(open('cal_data.p',"rb"))
    mtx = camera_cal["mtx"]
    dist = camera_cal["dist"]
except:
    print ('Calibration data does not exist')

capture(outDir, fileName, mtx, dist)

