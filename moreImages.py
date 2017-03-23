# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 09:37:01 2016

@author: shubham
"""
import random
import cv2
import os
import numpy
import math
import matplotlib.pyplot as plt
num_images = 270

def euler_to_mat(yaw, pitch, roll):
    # Rotate clockwise about the Y-axis
    c, s = math.cos(yaw), math.sin(yaw)
    M = numpy.matrix([[  c, 0.,  s],
                      [ 0., 1., 0.],
                      [ -s, 0.,  c]])

    # Rotate clockwise about the X-axis
    c, s = math.cos(pitch), math.sin(pitch)
    M = numpy.matrix([[ 1., 0., 0.],
                      [ 0.,  c, -s],
                      [ 0.,  s,  c]]) * M

    # Rotate clockwise about the Z-axis
    c, s = math.cos(roll), math.sin(roll)
    M = numpy.matrix([[  c, -s, 0.],
                      [  s,  c, 0.],
                      [ 0., 0., 1.]]) * M

    return M

def make_affine_transform(from_shape, to_shape, 
                          min_scale, max_scale,
                          scale_variation=1.0,
                          rotation_variation=1.0,
                          translation_variation=1.0):
    out_of_bounds = False

    from_size = numpy.array([[from_shape[1], from_shape[0]]]).T
    to_size = numpy.array([[to_shape[1], to_shape[0]]]).T

    scale = random.uniform((min_scale + max_scale) * 0.5 -
                           (max_scale - min_scale) * 0.5 * scale_variation,
                           (min_scale + max_scale) * 0.5 +
                           (max_scale - min_scale) * 0.5 * scale_variation)
    if scale > max_scale or scale < min_scale:
        out_of_bounds = True
    roll = random.uniform(-0.3, 0.3) * rotation_variation
    pitch = random.uniform(-0.2, 0.2) * rotation_variation
    yaw = random.uniform(-1.2, 1.2) * rotation_variation

    # Compute a bounding box on the skewed input image (`from_shape`).
    M = euler_to_mat(yaw, pitch, roll)[:2, :2]
    h, w = from_shape
    corners = numpy.matrix([[-w, +w, -w, +w],
                            [-h, -h, +h, +h]]) * 0.5
    skewed_size = numpy.array(numpy.max(M * corners, axis=1) -
                              numpy.min(M * corners, axis=1))

    # Set the scale as large as possible such that the skewed and scaled shape
    # is less than or equal to the desired ratio in either dimension.
    scale *= numpy.min(to_size / skewed_size)

    # Set the translation such that the skewed and scaled image falls within
    # the output shape's bounds.
    trans = (numpy.random.random((2,1)) - 0.5) * translation_variation
    trans = ((2.0 * trans) ** 5.0) / 2.0
    if numpy.any(trans < -0.5) or numpy.any(trans > 0.5):
        out_of_bounds = True
    trans = (to_size - skewed_size * scale) * trans

    center_to = to_size / 2.
    center_from = from_size / 2.

    M = euler_to_mat(yaw, pitch, roll)[:2, :2]
    M *= scale
    M = numpy.hstack([M, trans + center_to - M * center_from])

    return M, out_of_bounds


for i in range(0,num_images):
    f=random.choice(os.listdir('logos/'))
    logoI = cv2.imread('logos/'+f)
    logo = cv2.cvtColor(logoI, cv2.COLOR_BGR2GRAY)
    #logo = cv2.resize(logo,(64,32)) 
    # the commented code can be used to add background to the image
   # fbg=random.choice(os.listdir('bgs/'))
   # logoI = cv2.imread('bgs/'+fbg)
   # bg = cv2.cvtColor(logoI, cv2.COLOR_BGR2GRAY)
   # bg = cv2.resize(bg,(128,64))    
    
    scale = 1;#random.randint(0,5)
    if scale!=0 and ((logo.shape[0]/scale)>10):  
      #  logo = cv2.resize(logo,(logo.shape[0]/scale,logo.shape[1]/scale))
        M, out_of_bounds = make_affine_transform(
                            from_shape=logo.shape,
                            to_shape=logo.shape,
                            min_scale=1,
                            max_scale=1,
                            rotation_variation=1.0,
                            scale_variation=1.5,
                            translation_variation=1.2)   
                            
        im = cv2.warpAffine(logo,M,logo.shape,255)
   #     im = cv2.resize(im,(128,64))
   #     x_offset=random.randint(1,bg.shape[1]-im.shape[1])
   #     y_offset=random.randint(1,bg.shape[0]-im.shape[0])
   #     bg[y_offset:y_offset+im.shape[0], x_offset:x_offset+im.shape[1]] = im
        print 'test/'+str(i)+'_'+f
        cv2.imwrite('test/'+str(i)+'_'+f, im)
    else:
     #   im= cv2.resize(logo,(128,64))
        print 'test/'+str(i)+'_'+f
        cv2.imwrite('test/'+str(i)+'_'+f, im)