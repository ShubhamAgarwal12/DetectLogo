# Identifying and Locating Logo

## Getting Started

This project will make you familiar to logo identification and matching using SIFT feature detector and descriptor. The page contains details about the approach and instructions to get the project up and running on your local machine with python.

## Approach
### Template Matching
The first thing thats comes to mind is template matching but considering different scales of of the probe
images and logos, this will not be efficient. Somehow if we are able to detect the logo, then also we
will be facing difficulty in drawing the bounding box. We need to take into account the scaling for sure.
One more problem is that we will need a threshold so that we do not detect template in probe image
without any logo. We can set some threshold for current set of images but for scalability that's not a
good idea.

### SIFT
Considering the shortcomings of the template matching, a keypoint based detector seems to be a much
better approach. I tried using the SIFT detector and discriptor from OpenCV in python. SIFT feature
discriptor is scale, rotation and translation invariant so we can get better results compared to the
template matching case. To account for skewness I used the skewed synthetic images as part of the augmented dataset. Once we get good enough matches, we can compute corresponding homography to get
the bounding box in the probe image. More details on the code can be found at http://docs.opencv.org/2.4/doc/tutorials/features2d/feature_homography/feature_homography.html. This approach is scalable as once we add new logos, we can just
add the corresponding keypoints and label and utilize the same code.

### Some Results
![alt tag](https://github.com/ShubhamAgarwal12/findLogo/blob/master/FewResults/FoundStarbucks.PNG)

![alt tag](https://github.com/ShubhamAgarwal12/findLogo/blob/master/FewResults/FoundIntel.PNG)

### Not So Good Results

![alt tag](https://github.com/ShubhamAgarwal12/findLogo/blob/master/FewResults/FoundFord.PNG)

![alt tag](https://github.com/ShubhamAgarwal12/findLogo/blob/master/FewResults/FoundCoke.PNG)

## Getting the code running on your machine

### Prerequisites

The code is developed on Python2.7 with libraries OpenCV, numpy, random and math. This should work fine with later python versions with minor changes.

### Steps to replicate my results
1. Clone/copy the project files in your project directory.
2. Download the logo_data zip file from https://www.dropbox.com/s/n1ztszc3ut88d4h/logo_data.zip?dl=0 and extract it in the folder containing the python files.
3. In the project folder create directories to store the augmented dataset and the results.
    mkdir augmentedData
    mkdir matchResults
4. Run the file 'augmentData.py'. This will create an augmented dataset of the logos provided in logo_data. You can selecte the number of    images by configuring the variable num_images in the code file.
5. Now run 'logoMatch.py file. This will go throught he probe images and identify if they contain any logo. If logo is present, it will draw a bounding box at the locationit found the matching features. The resulting images will be stored in matchResults folder.

With this approach, I was able to get 61.11% of accuracy on the probe data with 27 logos. Note that half of the probe images don not contain any of the logo.
