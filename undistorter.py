import cv2 as cv
import numpy as np
import pickle

class Undistorter(object):

    def __init__(self, calFile='') -> None:
        self.calFile = calFile

    def cal_load(self, calFile):
        # Loading calibration data
        try:
            calData = pickle.load(open(calFile,"rb"))
            mtx = calData["mtx"]
            dist = calData["dist"]
            return [mtx, dist]
        except:
            print ('Calibration data does not exist')

    def undistort(self, img):
        try:
            # Load cal data
            mtx, dist = self.cal_load(self.calFile)
            # Undistort image with camera calibration data
            img_cor = cv.undistort(img, mtx, dist, None, mtx)
            return img_cor
        except:
            print ('Error. Possible cause: calibration data not found.')


