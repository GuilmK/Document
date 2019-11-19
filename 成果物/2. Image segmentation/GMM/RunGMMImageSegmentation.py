# -*- coding: utf-8 -*-
'''
使用sklearn库中的高斯混合模型 GaussianMixture和k-均值KMeans方法对图像进行分割
'''

import numpy as np

import time
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy import misc
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs


########### Learns a MoG model using the EM-algorithm for image-segmentation. 
from sklearn.mixture import GaussianMixture


############ Performs k-means clusering on the pixel values of an image. Used for color-quantization/compression.#####
from sklearn.cluster import KMeans
import sklearn


def kmeans_colors(img, k, max_iter=100):
    """
    Performs k-means clusering on the pixel values of an image.
    Used for color-quantization/compression.
    Args:
        img: The input color image of shape [h, w, 3]
        k: The number of color clusters to be computed
    Returns:
        img_cl:  The color quantized image of shape [h, w, 3]
    """

    img_cl = None

    #######################################################################
    # TODO:                                                               #
    # Perfom k-means clustering of the pixel values of the image img.     #
    #######################################################################
    img = np.array(img, dtype=np.float64) / 255
    w, h, d = tuple(img.shape)
    image_array = np.reshape(img, (w * h, d))

    # Fitting model on a small sub-sample of the data
    image_array_sample = sklearn.utils.shuffle(image_array, random_state=0)[:1000]

    # In this case n_clusters is the amount of colors
    kmeans = KMeans(n_clusters=k, random_state=0, max_iter=max_iter).fit(image_array_sample)

    labels = kmeans.predict(image_array)

    # Reproduce the picture
    img_cl = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            img_cl[i][j] = kmeans.cluster_centers_[labels[label_idx]]
            label_idx += 1

    return img_cl

############### Learns a MoG model using the EM-algorithm for image-segmentation #####################################
def em_segmentation(img, k, max_iter=20):
    """
    Learns a MoG model using the EM-algorithm for image-segmentation.
    Args:
        img: The input color image of shape [h, w, 3]
        k: The number of gaussians to be used
    Returns:
        label_img: A matrix of labels indicating the gaussian of size [h, w]
    """

    labels = None

    #######################################################################
    # TODO:                                                               #
    # 1st: Augment the pixel features with their 2D coordinates to get    #
    #      features of the form RGBXY (see np.meshgrid)                   #
    # 2nd: Fit the MoG to the resulting data using                        #
    #      sklearn.mixture.GaussianMixture                                #
    # 3rd: Predict the assignment of the pixels to the gaussian and       #
    #      generate the label-image                                       #
    #######################################################################

    # 1 preparations
    w = img.shape[1]
    h = img.shape[0]
    cols = img.shape[2]

    xgrid, ygrid = np.meshgrid(np.arange(0, w, 1), np.arange(0, h, 1))

    coordinates = np.stack((ygrid, xgrid), axis=2)
    img = np.concatenate((img, coordinates), axis=2)

    img = np.reshape(img, (h * w, cols + 2))

    # 2 fit the MoG
    moG = GaussianMixture(n_components=k).fit(img)

    label_img = moG.predict(img)

    means = np.delete(moG.means_, [3, 4], axis=1).astype('uint8')

    img_temp = np.take(means, label_img, axis=0)
    labels = np.reshape(img_temp, (h, w, cols))

    return labels

###################################################################################################################

# Load and show test image
img = misc.imread('zebra.jpg')
#img = misc.imread('dif_hand.jpg')
plt.imshow(img)
plt.title("Original image")
plt.show()

##### K-means segmentation
k = 2
img_cl = kmeans_colors(img, k)
###### Show the quantized image
plt.imshow(img_cl)
plt.title("k-means segmentation result")
plt.savefig('kMeansSegmentationImage.png', dpi=300) #保存图像
plt.show()


############ Test your implementation
k = 2
img_cl = em_segmentation(img, k, max_iter=50)

#### Show the quantized image
plt.imshow(img_cl)
plt.title("GMM segmentation result using EM")
plt.savefig('GMMSegmentationImage.png', dpi=300) #保存图像
plt.show()
