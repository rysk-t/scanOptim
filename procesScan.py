#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import os
import glob
import time

import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
from skimage import data, img_as_float
from skimage import exposure
from skimage import io
from skimage import transform

scale = 0.75

# function for escape []
def escapeBraceForGlob(str):
    # convert [ -> [[]  ,  ] -> []]
    newStr = str.replace("[","\\[").replace("]","\\]")
    newStr = newStr.replace("\\[","[[]").replace("\\]","[]]")
    return newStr


# script for optimize contrast of scanned book
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
path = sys.argv
rawpath = path[1]
path = escapeBraceForGlob(rawpath)
print "run at: " + path

if os.path.exists(rawpath[0:-1]+"_re/")==True:
    print "directory exist"
else:
    os.mkdir(rawpath[0:-1]+"_re/")

# Image processing
i = 1
t = time.time()
for file in glob.glob(path+'/*.jpg'):
    print(file)
    savefilename = "re_"+"{0:04d}".format(i)+".jpg"
    print "=>: " + savefilename    

    # image loading & processing
    img = io.imread(file, 0)
    #    plt.hist(img.ravel(), 128)
    #    plt.show()
    
    # discriminate color page
    if img.shape[2]==3:
        # imzR = stats.mstats.zscore(img[0:,0:,0].ravel())
        # imzG = stats.mstats.zscore(img[0:,0:,1].ravel())
        # imzB = stats.mstats.zscore(img[0:,0:,2].ravel())
        # buf, p1 = stats.wilcoxon(imzR,imzG)
        # buf, p2 = stats.wilcoxon(imzG,imzB)
        # buf, p3 = stats.wilcoxon(imzB,imzR)
        # r = np.corrcoef(imzR,imzB)
        # r2 = np.corrcoef(imzR,imzG)
        grayim = True
    else:
        grayim = True
        
    # print np.median(imzR) #np.median(img[0:,0:,0].ravel())
    # print np.median(imzG) #np.median(img[0:,0:,1].ravel())
    # print np.median(imzB) #np.median(img[0:,0:,2].ravel())
    # print r,r2

    # if (p1 < 0.05) | (p2 < 0.05) | (p3 < 0.05):
    #     grayim = False
    #     print "Color!"
    # else:
    #     grayim = True
    #     img = np.mean(img, 2)
    #     print "Gray!"
        
    p2, p98 = np.percentile(img, (1, 85))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))
    scaleShape = scale*np.array(img_rescale.shape)
    scaleShape = scaleShape.astype(np.int32)    
    scaleShape[2] = 3;
    img_rescale = transform.resize(img_rescale, scaleShape)
    io.imsave(rawpath[0:-1]+"_re/"+savefilename, img_rescale)
    i = i+1

print "======Complete Batch ====== "    

# Report time elapsed
elapsed = time.time() - t
print("{0:04f}".format(elapsed)+"[sec]/ "+"{0:04d}".format(i)+" [frames]")

