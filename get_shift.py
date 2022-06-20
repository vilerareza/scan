import os
import cv2 as cv
import numpy as np
import time
import pickle

imgDir = "img_corrected"

def thresholding(img, threshold=50):
    it = np.nditer(img, flags = ['multi_index'], op_flags = ['readwrite']) #iterator
    for x in it:
        if (x < threshold):
            x[...] = 0
        else:
            x[...] = 255
    return img

def find_tray_edge (edge_pixels):
    # Return the estimated tray position: transition between 0 (black) to 255 (white)
    i = 0    
    for pixel in edge_pixels:
        if pixel == 255:
            return i
        i+=1

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
        imageFiles = os.listdir(imgDir)
        if len(imageFiles) > 0:
            imgs = []
            tray_edges = []
            for i in range(len(imageFiles)):
                filePath = os.path.join(imgDir, f'{i}.png')
                img = cv.imread(filePath)
                imgs.append(img)
                # Find the image edges and threshold it to 0 or 255
                if (i % 2):
                    # If even image the top edge
                    edge = thresholding(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[0,::], threshold = 50)
                else:
                    # Edd image take the bottom edge
                    edge = thresholding(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[-1,::], threshold = 50)
                # Find tray edge
                tray_edge = find_tray_edge(edge)
                tray_edges.append(tray_edge)
            
            if len(tray_edges) > 1:
                shifts = []
                for i in range(len(tray_edges)-1):
                    shift = tray_edges[i+1]-tray_edges[i]
                    shifts.append(shift)
                #Accumulate the shift
                for i in range(len(shifts)-1):
                    shifts[i+1] = shifts[i+1]+shifts[i]
            
            pickle.dump(shifts, open('alignment_shifts.p', 'wb'))


        else:
            return False

    except Exception as e:
        print (e)
        return False

align_and_stack(imgDir)