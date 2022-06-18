import os
import cv2 as cv
import numpy as np
import pickle

checker_img_folder = '../checkerimages'
checker_corners = (7,7)
sq_size = 0.006
cal_resize_ratio = 5

object_points = []
img_points = []

objp = np.zeros((checker_corners[0]*checker_corners[1],3), np.float32)
objp[:,:2] = np.mgrid[0:7, 0:7].T.reshape(-1,2)
objp = objp*sq_size

# Reading checker images

imageFiles = os.listdir(checker_img_folder)
if len(imageFiles) > 0:
    for imageFile in imageFiles:
        filePath = os.path.join(checker_img_folder, imageFile)
        img = cv.imread(filePath)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Resize
        img_r = cv.resize(img, (int(img.shape[1]/cal_resize_ratio), int(img.shape[0]/cal_resize_ratio)))
        # Find corners
        retval, corners = cv.findChessboardCorners(img_r, checker_corners, cv.CALIB_CB_ADAPTIVE_THRESH+cv.CALIB_CB_NORMALIZE_IMAGE+cv.CALIB_CB_FAST_CHECK)
        if retval:
            object_points.append(objp)
            img_points.append(corners*cal_resize_ratio)
            print (f'Done {filePath}')
    try:
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_points, img_points, img.shape, None, None)
    except:
        print ('Calibration failed')

    # Serialize calibration data
    camera_cal = {}
    camera_cal["mtx"] = mtx
    camera_cal["dist"] = dist

    pickle.dump(camera_cal, open('../camera_cal.p', 'wb'))
else:
    print ('No checker images found')
