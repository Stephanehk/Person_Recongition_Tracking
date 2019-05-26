from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import timeit


def video_face_recognition(targets, video_path):
    image_path = "/Users/2020shatgiskessell/Downloads/Adrian-cropped.jpg"
    #OpenCV modules
    detector_p = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/face_detection_model/"
    embedding_model_p = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/embed/openface.nn4.small2.v1.t7"
    #output from previously files
    recognizer_p = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/output/recognizer.pickle"
    le_p = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/output/le.pickle"

    min_confidence = 0.5

    # load our serialized face detector from disk
    print("[INFO] loading face detector...")
    protoPath = os.path.sep.join([detector_p, "deploy.prototxt"])
    modelPath = os.path.sep.join(
        [detector_p, "res10_300x300_ssd_iter_140000.caffemodel"])
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    # load our serialized face embedding model from disk
    print("[INFO] loading face recognizer...")
    embedder = cv2.dnn.readNetFromTorch(embedding_model_p)

    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open(recognizer_p, "rb").read())
    le = pickle.loads(open(le_p, "rb").read())

    # # initialize the video stream, then allow the camera sensor to warm up
    print("[INFO] starting video processing...")
    # vs = VideoStream(src=0).start()
    # time.sleep(2.0)
    #
    # # start the FPS throughput estimator
    # fps = FPS().start()
    cap = cv2.VideoCapture(video_path)
    #cap = cv2.VideoCapture("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/real_training_data/Target1/IMG_0665.m4v")

    #store bounding box star coordinates
    startXs = {}
    startYs = {}

    # loop over frames from the video file stream
    start = timeit.default_timer()
    while cap.isOpened():
        # grab the frame from the threaded video stream
        ret, frame = cap.read()

        # resize the frame to have a width of 600 pixels (while maintaining the aspect ratio), and then grab the image dimensions
        try:
            frame = imutils.resize(frame, width=600)
        except AttributeError:
            break
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()
        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections
            if confidence > min_confidence:
                # compute the (x, y)-coordinates of the bounding box for
                # the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]
                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue
            # construct a blob for the face ROI, then pass the blob
                # through our face embedding model to obtain the 128-d
                # quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                 (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # perform classification to recognize the face
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]
                stop = timeit.default_timer()
                time_elapsed = start - stop
                # print ("name " + str(name))
                # print ("target " + str(target))

                if name in targets:
                    # print ("found a face at appropriate time")
                    # print (i)
                    startXs["target" + str(time_elapsed)] = startX
                    startYs["target" + str(time_elapsed)] = startY
                    cv2.imwrite(os.path.join("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/tracked_people" , 'target'+str(time_elapsed)+'.jpg'), frame)

            # elif i%20 == 0:
            #     startXs["other" + str(i) + "," + str(start)] = startX
            #     startYs["other" + str(i) + "," + str(start)] = startY
            #     cv2.imwrite(os.path.join("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/tracked_people" , 'unkown'+str(i)+'.jpg'), frame)

                # draw the bounding box of the face along with the
                # associated probability
                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # update the FPS counter
        #fps.update()
        # show the output frame
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
        #key = cv2.waitKey(1) & 0xFF

        # # if the `q` key was pressed, break from the loop
        # if key == ord("q"):
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break

    # stop the timer and display FPS information
    # fps.stop()
    # print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    # print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    #vs.stop()
    #check to see if target was recognized
    was_recognized = False
    if len(startXs):
        was_recognized = True
    return was_recognized, startXs, startYs
