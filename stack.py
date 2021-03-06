import os
import cv2 as cv
import numpy as np
import time

imgDir = "img_corrected"
threshold = 75

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
        pad = np.zeros((img.shape[0],int(abs(shift)),img.shape[2])).astype('uint8')
        # Ignore pixel from right
        img = img[::, :-abs(shift), ::]
        # Add pixel to left
        img = np.hstack((pad, img)).astype('uint8')
    else:
        # Shift left
        pad = np.zeros((img.shape[0],int(abs(shift)),img.shape[2])).astype('uint8')
        # Ignore pixel from left
        img = img[::, abs(shift):, ::]
        # Add pixel to right
        img = np.hstack((img, pad)).astype('uint8')
    
    return img

def stack_image(imgs = []):
    # Stack all the images in the array
    return np.vstack([img for img in imgs][::-1])

def align_and_stack(imgDir, threshold):
    try:
        imageFiles = os.listdir(imgDir)
        if len(imageFiles) > 0:
            imgs = []
            tray_edges_t = []
            tray_edges_b = []
            for i in range(len(imageFiles)):
                filePath = os.path.join(imgDir, f'{i}.png')
                img = cv.imread(filePath).astype('uint8')
                imgs.append(img.astype('uint8'))
                # Find the image edges and threshold it to 0 or 255
                edge_t = thresholding(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[0,::], threshold)
                edge_b = thresholding(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[-1,::], threshold)
                tray_edge_t = find_tray_edge(edge_t)
                tray_edge_b = find_tray_edge(edge_b)
                tray_edges_t.append(tray_edge_t)
                tray_edges_b.append(tray_edge_b)
            
            shifts = []
            for i in range(len(imgs)-1):
                shift = tray_edges_b[i+1]-tray_edges_t[i]
                shifts.append(shift)

            #Accumulate the shift
            for i in range(len(shifts)-1):
                shifts[i+1] = shifts[i+1]+shifts[i]

            # Shift the images (except image 0)
            for i in range(len(imgs)):
                if i > 0:
                    imgs[i]=shift_image(imgs[i], shifts[i-1]).astype('uint8')
            # Output
            outimg = stack_image(imgs)
            return outimg
        else:
            return []

    except Exception as e:
        print (e)
        return []

def post_process ():
    global imgDir
    global threshold
    t1 = time.time()
    outImg = align_and_stack(imgDir, threshold)
    outFileName = f'Scan_{time.strftime("%Y-%m-%d_%H-%M-%S")}.png'
    if len(outImg) > 0:
        cv.imwrite(outFileName, outImg)
        t2 = time.time()
        print (f'Post-processing done. Timelapse: {t2-t1}s')
        return True
    else:
        t2 = time.time()
        print (f'Post-processing failed...')
        return False
'''
class Stacker(object):
    
    def __init__(self, nImages, imgDir, condition) -> None:
        self.nImages = nImages
        self.imgDir = imgDir
        self.condition = condition
    
    def thresholding(self, img, threshold=50):
        it = np.nditer(img, flags = ['multi_index'], op_flags = ['readwrite']) #iterator
        for x in it:
            if (x < threshold):
                x[...] = 0
            else:
                x[...] = 255
        return img

    def find_tray_edge (self, edge_pixels):
        # Return the estimated tray position: transition between 0 (black) to 255 (white)
        i = 0    
        for pixel in edge_pixels:
            if pixel == 255:
                return i
            i+=1

    def shift_image(self, img, shift):
        if shift < 0:
            # Shift right
            pad = np.zeros((img.shape[0],int(abs(shift)),img.shape[2])).astype('uint8')
            # Ignore pixel from right
            img = img[::, :-abs(shift), ::]
            # Add pixel to left
            img = np.hstack((pad, img)).astype('uint8')
        else:
            # Shift left
            pad = np.zeros((img.shape[0],int(abs(shift)),img.shape[2])).astype('uint8')
            # Ignore pixel from left
            img = img[::, abs(shift):, ::]
            # Add pixel to right
            img = np.hstack((img, pad)).astype('uint8')
        
        return img

    def stack_image(self, imgs = []):
        # Stack all the images in the array
        return np.vstack([img for img in imgs][::-1])

    def align_and_stack(self, imgDir):
        try:
            if self.nImages > 0:
                imgs = []
                tray_edges_t = []
                tray_edges_b = []
                for i in range(self.nImages):
                    with self.condition:
                        # wait until the last capture is completed
                        print ('Waiting for scan image')
                        self.condition.wait()
                    filePath = os.path.join(imgDir, f'{i}.png')
                    img = cv.imread(filePath).astype('uint8')
                    imgs.append(img.astype('uint8'))
                    # Find the image edges and threshold it to 0 or 255
                    edge_t = self.thresholding(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[0,::])
                    edge_b = self.thresholding(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[-1,::])
                    tray_edge_t = self.find_tray_edge(edge_t)
                    tray_edge_b = self.find_tray_edge(edge_b)
                    tray_edges_t.append(tray_edge_t)
                    tray_edges_b.append(tray_edge_b)
                
                shifts = []
                for i in range(len(imgs)-1):
                    shift = tray_edges_b[i+1]-tray_edges_t[i]
                    shifts.append(shift)

                #Accumulate the shift
                for i in range(len(shifts)-1):
                    shifts[i+1] = shifts[i+1]+shifts[i]

                # Shift the images (except image 0)
                for i in range(len(imgs)):
                    if i > 0:
                        imgs[i]=self.shift_image(imgs[i], shifts[i-1]).astype('uint8')
                # Output
                outimg = self.stack_image(imgs)
                return outimg
            else:
                return []

        except Exception as e:
            print (e)
            return []

    def post_process (self):
        t1 = time.time()
        outFileName = f'Scan_{time.strftime("%Y-%m-%d_%H-%M-%S")}.png'
        outImg = self.align_and_stack(self.imgDir)
        if len(outImg) > 0:
            cv.imwrite(outFileName, outImg)
            t2 = time.time()
            print (f'Post-processing done. Timelapse: {t2-t1}s')
            return True
        else:
            t2 = time.time()
            print (f'Post-processing failed...')
            return False
'''