# Identifying and Locating Logo

## Getting Started

This project will make you familiar to logo identification and matching using SIFT feature detector and descriptor. The page contains details about the approach and instructions to get the project up and running on your local machine with python.

### Prerequisites

The code is developed on Python2.7 with libraries OpenCV, numpy, random and math. This should work fine with later python versions with minor changes.

### Approach



## Getting the code running on your machine
1. Clone/copy the project files in your project directory.
2. Download the logo_data zip file from https://www.dropbox.com/s/n1ztszc3ut88d4h/logo_data.zip?dl=0 and extract it in the folder containing the python files.
3. In the project folder create directories to store the augmented dataset and the results.
    mkdir augmentedData
    mkdir matchResults
4. Run the file 'augmentData.py'. This will create an augmented dataset of the logos provided in logo_data. You can selecte the number of    images by configuring the variable num_images in the code file.
5. Now run 'logoMatch.py file. This will go throught he probe images and identify if they contain any logo. If logo is present, it will draw a bounding box at the locationit found the matching features. The resulting images will be stored in matchResults folder.

With this approach, I was able to get 61.11% of accuracy on the probe data with 27 logos. Note that half of the probe images don not contain any of the logo.
