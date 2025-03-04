# Import necessary functions

import cv2
import matplotlib.pyplot as plt
import numpy as np

from opts import get_opts
# Import necessary functions
from planarH import computeH_ransac, compositeH_full
from displayMatch import displayMatched
from helper import plotMatches

# Q4
path1 = '../data/left.jpg'
path2 = '../data/right.jpg'
opts = get_opts()
ratio = opts.ratio  # 'ratio for BRIEF feature descriptor'
sigma = opts.sigma  # 'threshold for corner detection using FAST feature detector'

# Read the image and convert to grayscale, if necessary
I1 = cv2.imread(path1)

I2 = cv2.imread(path2)

# ctrpts = cpselect(path1, path2)
# print(controlpointlist)
ctrpts = [{'point_id': 1, 'img1_x': 711.311660866606, 'img1_y': 327.3734452360825, 'img2_x': 244.2249892964178,
           'img2_y': 349.979410699191},
          {'point_id': 2, 'img1_x': 693.9224566642149, 'img1_y': 271.7279917884314, 'img2_x': 230.31362593450513,
           'img2_y': 287.37827557058336},
          {'point_id': 3, 'img1_x': 831.2971698631039, 'img1_y': 289.11719599082244, 'img2_x': 365.94941871315496,
           'img2_y': 334.32912691703905},
          {'point_id': 4, 'img1_x': 711.311660866606, 'img1_y': 476.9206013766453, 'img2_x': 237.26930761546146,
           'img2_y': 499.52656683975374},
          {'point_id': 5, 'img1_x': 829.5582494428648, 'img1_y': 449.09787465281977, 'img2_x': 362.4715778726768,
           'img2_y': 492.5708851587973},
          {'point_id': 6, 'img1_x': 704.3559791856495, 'img1_y': 541.2606569254922, 'img2_x': 230.31362593450513,
           'img2_y': 565.6055428088396},
          {'point_id': 7, 'img1_x': 815.6468860809521, 'img1_y': 520.393611882623, 'img2_x': 350.299134931003,
           'img2_y': 560.3887815481222},
          {'point_id': 8, 'img1_x': 826.0804086023867, 'img1_y': 833.3992875256613, 'img2_x': 350.299134931003,
           'img2_y': 868.1776959304433},
          {'point_id': 9, 'img1_x': 848.686374065495, 'img1_y': 958.6015577828766, 'img2_x': 362.4715778726768,
           'img2_y': 988.1632049269413},
          {'point_id': 10, 'img1_x': 728.700865068997, 'img1_y': 911.6507064364208, 'img2_x': 239.00822803570054,
           'img2_y': 944.6901944209637},
          {'point_id': 11, 'img1_x': 796.5187614583219, 'img1_y': 897.739343074508, 'img2_x': 312.04288568574293,
           'img2_y': 930.778831059051},
          {'point_id': 12, 'img1_x': 728.700865068997, 'img1_y': 939.4734331602465, 'img2_x': 240.74714845593962,
           'img2_y': 981.2075232459849},
          {'point_id': 13, 'img1_x': 645.2326848975201, 'img1_y': 953.3847965221594, 'img2_x': 148.58436618326732,
           'img2_y': 1005.5524091293323},
          {'point_id': 14, 'img1_x': 648.7105257379983, 'img1_y': 922.0842289578554, 'img2_x': 148.58436618326732,
           'img2_y': 969.0350803043112},
          {'point_id': 15, 'img1_x': 546.1142209438913, 'img1_y': 939.4734331602465, 'img2_x': 23.38209592605199,
           'img2_y': 998.596727448376},
          {'point_id': 16, 'img1_x': 544.3753005236522, 'img1_y': 977.7296824055068, 'img2_x': 19.904255085573595,
           'img2_y': 1038.5918971138753},
          {'point_id': 17, 'img1_x': 937.3713154976891, 'img1_y': 1252.4791088032848, 'img2_x': 430.2894742620017,
           'img2_y': 1271.607233425915},
          {'point_id': 18, 'img1_x': 572.1980272474779, 'img1_y': 1092.4984301412874, 'img2_x': 44.24914096892121,
           'img2_y': 1167.2720082115688},
          {'point_id': 19, 'img1_x': 763.479273473779, 'img1_y': 664.7240067624683, 'img2_x': 285.95907938215623,
           'img2_y': 701.2413355874895},
          {'point_id': 20, 'img1_x': 801.7355227190393, 'img1_y': 711.6748581089241, 'img2_x': 327.6931694678947,
           'img2_y': 746.4532665137061},
          {'point_id': 21, 'img1_x': 707.8338200261278, 'img1_y': 624.7288370969691, 'img2_x': 226.83578509402673,
           'img2_y': 649.0737229803165},
          {'point_id': 22, 'img1_x': 704.3559791856495, 'img1_y': 706.4580968482069, 'img2_x': 226.83578509402673,
           'img2_y': 741.2365052529889},
          {'point_id': 23, 'img1_x': 886.9426233107553, 'img1_y': 607.339632894578, 'img2_x': 411.16134963937156,
           'img2_y': 642.11804129936},
          {'point_id': 24, 'img1_x': 879.9869416297988, 'img1_y': 704.7191764279677, 'img2_x': 405.9445883786543,
           'img2_y': 734.2808235720324},
          {'point_id': 25, 'img1_x': 899.115066252429, 'img1_y': 469.964919695689, 'img2_x': 423.3337925810454,
           'img2_y': 511.69900978142743},
          {'point_id': 26, 'img1_x': 940.8491563381674, 'img1_y': 457.7924767540152, 'img2_x': 461.59004182630565,
           'img2_y': 509.96008936118835},
          {'point_id': 27, 'img1_x': 900.853986672668, 'img1_y': 562.1277019683614, 'img2_x': 421.5948721608063,
           'img2_y': 605.6007124743389},
          {'point_id': 28, 'img1_x': 946.0659175988847, 'img1_y': 560.3887815481222, 'img2_x': 465.0678826667838,
           'img2_y': 607.339632894578},
          {'point_id': 29, 'img1_x': 987.8000076846231, 'img1_y': 509.96008936118835, 'img2_x': 503.3241319120441,
           'img2_y': 560.3887815481222}]

locs1, locs2 = [], []

for i in ctrpts:
    id = i['point_id']
    x1 = i['img1_x']
    y1 = i['img1_y']
    x2 = i['img2_x']
    y2 = i['img2_y']
    locs1.append([y1, x1])
    locs2.append([y2, x2])
loc1_, loc2_ = np.array(locs1), np.array(locs2)

bestH2to1, inliers = computeH_ransac(loc1_, loc2_, opts)

plotMatches(I1, I2, np.array([[i, i] for i in range(len(loc1_))]), loc1_, loc2_)

composite_img = compositeH_full(bestH2to1, I1, I2)
composite_img = composite_img[:, :, [2, 1, 0]]

plt.imshow(composite_img)
plt.show()
