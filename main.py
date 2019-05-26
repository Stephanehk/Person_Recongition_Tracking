import cv2
import numpy as np

import extract_facial_embeddings
import model_training
import image_face_recognizer
import video_face_recognizer
import video_face_recognizer_upload
import plot_matrix
import count_people
import get_population_density

def run_everything(video_path, lat,long):
    #training lines
    # extract_facial_embeddings.find_facial_embeddings()
    # model_training.train_face_recognizer()

    #run face recogntion
    was_recognized, startXs, startYs = video_face_recognizer_upload.video_face_recognition(["Jake", "Target2", "Target4"],video_path)
    #analyse found people
    avg_num_people, avg_distance = count_people.count_people(startXs, startYs)
    # print("avg ppl " + str(avg_num_people))
    # print("avg dist " + str(avg_distance))

    pop_count, name = get_population_density.population_den(lat,long)

    search_area, dists = plot_matrix.run(int(pop_count),50)

    print ("Area: " + str(name))
    if was_recognized:
        print ("POI located")
    else:
        print ("POI not found")
    # #arbitrary number
    if int(avg_num_people) != 0:
        avg_num_people = round(avg_num_people) - 1

    print ("People near POI: " + str(avg_num_people))

    if avg_distance > 1000 or avg_num_people == 0:
        print ("POI seems to be alone")
    else:
        print ("POI likely with someone")

    cv2.imshow("search_area", search_area)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

run_everything("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/real_training_data2/IMG_0713.m4v", 40.777209,-73.979910)
