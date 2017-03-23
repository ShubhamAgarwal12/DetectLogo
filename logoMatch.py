# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 21:28:05 2016

@author: shubham
"""

import cv2
import numpy as np
import os
 
detector = cv2.xfeatures2d.SIFT_create(60)

uarray=[4]              #can be used to tune hyper parameters
tharray = [0.65]
for u in uarray:
    for th in tharray:
        i=0
        kps2 =[]
        descs2 =[]
        brand =[]
        MAX_LIMIT =1
        files=os.listdir('logos/')
        # store the descriptors for all the logos
        for f in files:
                logoI = cv2.imread('logos/'+f)
                logo = cv2.cvtColor(logoI, cv2.COLOR_BGR2GRAY)
                (kps, descs) = detector.detectAndCompute(logo, None)
                kps2.append(kps)
                descs2.append(descs)
                brand.append(f.split('.')[0])
                
        files=os.listdir('test_Shubham/')
        
        for f in files:             # add synthetic images to the logos
                logoI = cv2.imread('test_Shubham/'+f)
                logo = cv2.cvtColor(logoI, cv2.COLOR_BGR2GRAY)
                (kps, descs) = detector.detectAndCompute(logo, None)
                kps2.append(kps)
                descs2.append(descs)
                brand.append(f.split('_')[1].split('.')[0])
        
        # read probes.txt file
        with open('probes.txt') as f:
            lines = f.readlines()
        detector = cv2.xfeatures2d.SIFT_create() 
        # process the probes.txt file line by line
        actualBrand=[]
        logoMatchList=[]
        for line in lines:
            hashMap={}
            logoMatch=[]
            filename = line.split("\t")[0]
            brandname = line.split("\t")[1].strip()
            probeI = cv2.imread('probes/'+filename);
            probe = cv2.cvtColor(probeI, cv2.COLOR_BGR2GRAY)
            detector = cv2.xfeatures2d.SIFT_create()
            (kps1, descs1) = detector.detectAndCompute(probe, None)
            i=0
            for d,kp in zip(descs2,kps2):
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(d,descs1,k=3)
        #
        #ratio test to identify good matches
                #FLANN_INDEX_KDTREE = 0
                #index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
                #search_params = dict(checks = 50)
        
                #flann = cv2.FlannBasedMatcher(index_params, search_params)
                good = []
                #matches = flann.knnMatch(d,descs1,k=2)
                
                for m,n,k in matches:
                    if m.distance < th*n.distance:# and m.distance < 0.5*k.distance:
                        good.append(m)
                good = sorted(good, key=lambda val: val.distance)
        
                if len(good)>u:
                    if hashMap.get(brand[i]) is None:
                        hashMap[brand[i]]=1
                    else:
                        break
                    src_pts = np.float32([ kp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                    dst_pts = np.float32([ kps1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
                    
                   # good = good[0:1]
                   # src_pts = np.float32([ kp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                   # dst_pts = np.float32([ kps1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
                    
                    #get homography to draw the bounding box
                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,8.0)
                    if mask is not None:            
                        matchesMask = mask.ravel().tolist()
                        logoMatch.append(brand[i])
                        h,w = logo.shape
                        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                        dst = cv2.perspectiveTransform(pts,M)
        
                        probe = cv2.polylines(probe,[np.int32(dst)],True,(0,0,255),3, cv2.LINE_AA)
                        cv2.imwrite('matchResults/'+filename+'_'+brand[i]+'1.png', probe)
                    else:
                        matchesMask = None
                i=i+1
            logoMatchList.append(logoMatch)
            actualBrand.append(brandname)
        
        # computing accuracy
        tp=0
        tn=0
        fp=0
        fn=0    
        i=0
        
        for brands in logoMatchList:
            for brand in brands:
                if(brand ==actualBrand[i]):
                    tp=tp+1
                else:
                    fp=fp+1
            i=i+1
        i=0
        
        for brands in logoMatchList:
            if (brands==[]):
                if (actualBrand[i]=='none'):
                    tn=tn+1
                else:
                    fn=fn+1
            i=i+1
        print "accuracy =" + str((float)(tp+tn)/(float)(tp+tn+fp+fn)) 