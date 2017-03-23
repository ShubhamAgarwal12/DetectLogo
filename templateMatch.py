# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:39:10 2016

@author: shubham
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt

template = cv2.imread('/home/shubham/Desktop/logo_spotting_problem/logos/apple.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
plt.imshow(template)

# loop over the images to find the template in

	# load the image, convert it to grayscale, and initialize the
	# bookkeeping variable to keep track of the matched region
image = cv2.imread('/home/shubham/Desktop/logo_spotting_problem/probes/51409302.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
found = None
 
	# loop over the scales of the image
for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
    newX,newY = gray.shape 
    resized = cv2.resize(gray, (int(newX*scale),int(newY*scale)))
    r = gray.shape[1] / float(resized.shape[1])
 
		# if the resized image is smaller than the template, then break
		# from the loop
    if resized.shape[0] < tH or resized.shape[1] < tW:
		break

		# detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
  
 
		# if we have found a new maximum correlation value, then ipdate
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
 
	# unpack the bookkeeping varaible and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
 
	# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
plt.imshow("Image", image)
cv2.waitKey(0)