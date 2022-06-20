import os
import cv2 as cv
import numpy as np
import time
import pickle

imgDir = "img_corrected"

def shift_image(img, shift):
    if shift < 0:
        # Shift right
        pad = np.zeros((img.shape[0],(abs(shift)),img.shape[2]))
        # Ignore pixel from right
        img = img[::, :-abs(shift), ::]
        # Add pixel to left
        img = np.hstack((pad, img))
    else:
        # Shift left
        pad = np.zeros((img.shape[0],(abs(shift)),img.shape[2]))
        # Ignore pixel from left
        img = img[::, abs(shift):, ::]
        # Add pixel to right
        img = np.hstack((img, pad))
    
    return img

def stack_image(imgs = []):
    # Stack all the images in the array
    return np.vstack([img for img in imgs][::-1])

def align_and_stack(imgDir):
    try:
        shifts = pickle.load(open('alignment_shifts.p',"rb"))
        imageFiles = os.listdir(imgDir)
        if len(imageFiles) > 0:
            imgs = []
            for i in range(len(imageFiles)):
                filePath = os.path.join(imgDir, f'{i}.png')
                img = cv.imread(filePath)
                imgs.append(img)
            for i in range(len(imgs)):
                if i > 0:
                    imgs[i]=(shift_image(imgs[i], shifts[i-1]))

            # Output
            outimg = stack_image(imgs)
            cv.imwrite('Scan.png', outimg)
            return True
        else:
            return False

    except Exception as e:
        print (e)
        return False

t1 = time.time()
align_and_stack(imgDir)
t2 = time.time()

print (f'Timelapse: {t2-t1}s')

# def stack():
#     try:
#         imageFiles = os.listdir(imgDir)
#         if len(imageFiles) > 0:
#             imgs = []
#             for i in range(len(imageFiles)):
#                 filePath = os.path.join(imgDir, f'{i}.png')
#                 img = cv.imread(filePath)
#                 imgs.append(img)
#             # Stack the images
#             stacked = np.vstack([img for img in imgs][::-1])
#             #img = img[::,800:-800,::]
#             cv.imwrite('Scan.bmp', stacked)
#             return True
#         else:
#             print('No images found')
#             return False

#     except Exception as e:
#         print (f'Error during image stacking: {e}')
#         return False

# stack()