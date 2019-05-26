import pprint
import random
import cv2
import plot_data
import numpy as np

def find_dist(dens, time):

    # print(dens)
    if dens >= 20000:
        speed = 15.2
    elif 19999 >= dens >= 10000:
        speed = 19.3
    elif 9999 >= dens >= 5000:
        speed = 24.2
    elif 4999 >= dens >= 3000:
        speed = 30.0
    elif 2999 >= dens:
        speed = 31.7
    else:
        speed = 31.7

    dist = time * speed
    return dist


def search_area(start, map, dens):
    dists = []
    count = 0
    time = 0
    for i in range(4):
        time = time + .25
        count = count + 1
        x,y = start
        dist = find_dist(dens, time)
        dists.append(dist)
        for row in range(len(map)):
            for col in range(len(map)):
                if np.sqrt(np.power((row - x),2)+ np.power((col - y),2)) <= dist:
                    if map[row][col] == 0:
                        map[row][col] = count
    return map, dists

def run(dens, size):
    map = [[random.randint(0,0) for row in range(size)] for col in range(size)]
    map, dists = search_area((size/2,size/2), map, dens)
    plot_data.plot(map,dists)
    img = cv2.imread("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/mapped_area.png")
    return img, dists
