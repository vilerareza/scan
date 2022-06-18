#import argparse
import os
import cv2 as cv
import numpy as np

imgDir = "img_corrected"

def stack():
    try:
        imageFiles = os.listdir(imgDir)
        if len(imageFiles) > 0:
            imgs = []
            for i in range(len(imageFiles)):
                filePath = os.path.join(imgDir, f'{i}.png')
                img = cv.imread(filePath)
                imgs.append(img)
            # Stack the images
            stacked = np.vstack([img for img in imgs][::-1])
            #img = img[::,800:-800,::]
            cv.imwrite('Scan.bmp', stacked)
            return True
        else:
            print('No images found')
            return False

    except Exception as e:
        print (f'Error during image stacking: {e}')
        return False

stack()