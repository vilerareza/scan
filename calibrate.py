import os
import cv2 as cv
import numpy as np
import pickle

checker_img_folder = 'checker'
checker_corners = (8,12)
sq_size = 0.02
cal_resize_ratio = 6.0
object_points = []
img_points = []

objp = np.zeros((checker_corners[0]*checker_corners[1],3), np.float32)
objp[:,:2] = np.mgrid[0:8, 0:12].T.reshape(-1,2)
objp = objp*sq_size

# Reading checker images

imageFiles = os.listdir(checker_img_folder)
if len(imageFiles) > 0:
    file_ok = []
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
            file_ok.append(filePath)
            print (f'Done {filePath}')
    try:
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_points, img_points, img.shape, None, None)
        # Refine cal data
        img = cv.imread(file_ok[0])
        h, w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
        # Serialize calibration data
        camera_cal = {}
        camera_cal["mtx"] = mtx
        camera_cal["dist"] = dist
        camera_cal["new_mtx"] = newcameramtx
        camera_cal["roi"] = roi
        pickle.dump(camera_cal, open('camera_cal.p', 'wb'))    
    except:
        print ('Calibration failed')

else:
    print ('No checker images found')
