import cv2
import numpy as np
import glob
import os
import math


def split_dict(dict1, target_key):
    target_vals = {}
    non_target_vals = {}
    for key, value in dict1.items():
        if target_key in key:
            target_vals[key] = value
        else:
            non_target_vals[key] = value
    # print ("Input dict")
    # print(dict1)
    # print ("Ouptput dicts")
    # print(target_vals)
    # print(non_target_vals)
    # print ("\n")
    return target_vals, non_target_vals

def calc_distance(targetxs, targetys, otherxs, otherys):
    total_dist = 0
    for i in range(len(targetxs)):
        try:
            tkey, tx = list(targetxs.items())[i]
            tx_time_stamp = tkey.split(",")[1]
            tkey, ty = list(targetys.items())[i]
            okey, ox = list(otherxs.items())[i]
            ox_time_stamp = okey.split(",")[1]
            okey, oy = list(otherys.items())[i]
        except IndexError:
            return total_dist
        # print ("timestamp: " + str(tx_time_stamp))
        # print ("timestamp: " + str(ox_time_stamp))

        if np.abs(float(tx_time_stamp) - float(ox_time_stamp)) < 3:
            distance = np.sqrt(np.power(ox-tx, 2) + np.power(oy-ty, 2))
        else:
            continue
        total_dist += distance
    return total_dist

def l2_dist (x1,y1,x2,y2):
    #print ("current face: " + str(x1) + "," + str(y1))
    #print ("target face: " + str(x2) + "," + str(y2))
    dist = np.sqrt(np.power(y2-y1,2) + np.power(x2-x1,2))
    return dist

def count_people(startXs, startYs):
    startXs = list(startXs.values())
    startYs = list(startYs.values())
    folder_path = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/tracked_people/*.jpg"
    images = [cv2.imread(file) for file in glob.glob(folder_path)]
    face_cascade = cv2.CascadeClassifier('/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/haarcascade_frontalface_default.xml')
    number_of_ppl = []
    distances = []
    for i in range(len(images)):
        image = images[i]
        try:
            target_X = startXs[i]
            target_Y = startYs[i]
        except IndexError:
            continue

        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grayImage)
        try:
            num_faces = faces.shape[0]
        except AttributeError:
            continue
        # target_valsx, non_target_valsx = split_dict(startXs, "target")
        # target_valsy, non_target_valsy = split_dict(startYs, "target")
        # distance = calc_distance(target_valsx, target_valsy, non_target_valsx, non_target_valsy)
        number_of_ppl.append(num_faces)
        #display faces
        if num_faces > 1:
             for (x,y,w,h) in faces:
                 distance = l2_dist (x,y,target_X,target_Y)
                 if distance != 0:
                     distances.append(distance)
             # cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
             #
             # cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), (255,255,255), -1)
             # cv2.putText(image, "Number of faces detected: " + str(faces.shape[0]), (0,image.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
             #
             # cv2.imshow('Image with faces',image)
             # cv2.waitKey(0)
             # cv2.destroyAllWindows()
    #delete everything in folder
    files = glob.glob(folder_path)
    for f in files:
        os.remove(f)

    #print("distance between objects "+str(distances))
    mean_n_ppl = np.mean(number_of_ppl)
    if math.isnan(mean_n_ppl):
        mean_n_ppl = 0

    return mean_n_ppl, np.mean(distances)
