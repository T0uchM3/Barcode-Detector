#import cv2
#cap = cv2.VideoCapture(0)
#while(cap.isOpened()):
# ret, frame = cap.read()
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# cv2.imshow('frame',gray)
# if cv2.waitKey(1) & 0xFF == ord('q'):
#    break
#cap.release()
#cv2.destroyAllWindows()


#import pyzbar
#import argparse
import cv2
#import numpy as np


import pyzbar.pyzbar as zbar
from PIL import Image
image = cv2.imread("img2.jpg")

#barcode = zbar.decode(Image.open("img2.png"))
barcode = zbar.decode(image)
print('ZBar: {}'.format(barcode[0].data.decode("utf-8")))

