
'''
The solution scheme is as follows:

1. Quantization of image pixel values (elimination of information noise). In practice, it can be 4 or 8 values for
each channel.

2. Construction of image feature vectors. In our case, for simplicity, these will be RGB (three-dimensional) histograms.

3. Determining the distance matrix of "each image to each other". Thus, by definition, it is a symmetric matrix: the
matrix element d_ij = d_ji, because the distance of image "i" to "j" is the same as image "j" to "i". At this stage,
each image is represented by its multidimensional vector (an element of vector space). Taking this into account, it
is possible to determine the (dis) similarity of two images as the distances of the vectors representing them.

4. The image that is most "similar" to the given input image is the image that minimizes the adopted definition of
the distance (information stored in the above-mentioned matrix).

Solution:
1. Search results for sample 5 images (each from a different subject category). For each of them, provide 3-5 most
similar images) and the designated distance values.

2. Present the results independently for the Euclidean and Manhattan distance.

Assume that the set of images are images that can be downloaded from http://wang.ist.psu.edu/docs/related/ (collection
of 1000 test images)
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance


rang = 1000 
imglist = []    
histlist = []
normalized_histlist = []
lowest_dist_dic = {}
lowest_dist_keys = []


def create_hist():
    for index in range(0, rang):
        path = "C:/Users/kwidz/Downloads/test1/image.orig/"+str(index)+".jpg"
        image_loaded = plt.imread(path)
        imglist.append(image_loaded)
        hist_dic = {(i,j,k): 0 for i in range(0,4) for j in range(0,4) for k in range(0,4)}
        image = image_loaded.copy()
        image = np.floor(image/64).astype(int)
        image = image.reshape(image.shape[0]*image.shape[1], 3)
        for i in range(0, image.shape[0]):
            hist_dic[image[i,0], image[i,1], image[i,2]] += 1
        hist_vec = np.array(list(hist_dic.values()))
        hist_vec = hist_vec / np.linalg.norm(hist_vec)
        histlist.append(hist_vec)    
    print('--- normalized histograms calculated ---')
    print()
    return histlist

def manhattan(index):
    print('--- manhattan metric distance from image {} calculated: ---'.format(int(index)))
    dist_dic_man = {i: 0 for i in range(0, rang)}
    for i in range (0, rang):
        dist_dic_man[i] = distance.cityblock(histlist[index], histlist[i])
    # print(dist_dic_man)
    return dist_dic_man

def euclidean(index):
    print('--- euclidean metric distance from image {} calculated: ---'.format(int(index)))
    dist_dic_euc = {i: 0 for i in range(0, rang)}
    for i in range (0, rang):
        dist_dic_euc[i] = distance.euclidean(histlist[index], histlist[i])
    # print(dist_dic_euc)
    return dist_dic_euc

def find_nearest(metrics):
    for j in range (0, 6):
        lowest_dist = min(metrics, key = metrics.get)
        x = lowest_dist
        y = metrics.pop(lowest_dist)
        lowest_dist_dic[x] = y  
    print('--- 5 nearest distances (image index: distance): ---')
    print(lowest_dist_dic)
    return lowest_dist_dic

def plot(dic):
    for key in dic.keys():
            lowest_dist_keys.append(key)
    f, ax = plt.subplots(1, 6, sharey = True, figsize = (25,25))
    for i in range(0, 6):
        ax[i].imshow(imglist[lowest_dist_keys[i]])
    print()
    return lowest_dist_keys


if __name__ == "__main__":
    
    
    ### creating histograms
    hist = create_hist()
   
    
    no = input('Input image index to compare: ')
    
    
    ### measuring manhattan distance
    man_measure = manhattan(int(no))
    ### finding five nearest 
    nearest_man = find_nearest(man_measure)
    ### plot
    plot_man = plot(nearest_man)
    nearest_man.clear()
    plot_man.clear()
    
    
    ### measuring euclidean distance
    euc_measure = euclidean(int(no))
    ### finding five nearest 
    nearest_euc = find_nearest(euc_measure)
    ### plot
    plot_euc = plot(nearest_euc)

    
    

    



    
    




    