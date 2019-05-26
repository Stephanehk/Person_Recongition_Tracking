from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

def find_facial_embeddings ():
    #load everything
    #dataset = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/dataset"
    dataset = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/real_training_data"
    # embeddings = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
    detector_path = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/face_detection_model/"
    embedding_model = "/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/embed/openface.nn4.small2.v1.t7"
    min_confidence = 0.5 #defualt confidence value

    print ("loading face detector")
    protoPath = os.path.sep.join([detector_path,"deploy.prototxt"])
    modelPath = os.path.sep.join([detector_path,"res10_300x300_ssd_iter_140000.caffemodel"])
    detector = cv2.dnn.readNetFromCaffe(protoPath,modelPath)

    print ("loading face recognizer")
    embedder = cv2.dnn.readNetFromTorch(embedding_model)

    print("quantifying faces...")
    imagePaths = list(paths.list_images(dataset))
    print (imagePaths)

    #keep track of everything
    knownEmbeddings = []
    knownNames = []

    #total number of faces
    total = 0

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

    	# load the image, resize it to have a width of 600 pixels (while
    	# maintaining the aspect ratio), and then grab the image
    	# dimensions
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=600)
        (h, w) = image.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
        		cv2.resize(image, (300, 300)), 1.0, (300, 300),
        		(104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector
        detector.setInput(imageBlob)
        detections = detector.forward()
        #process detections
        if len(detections) > 0:
            # we're making the assumption that each image has only ONE
            # face, so find the bounding box with the largest probability
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]

    		# ensure that the detection with the largest probability also
    		# means our minimum probability test (thus helping filter out
    		# weak detections)
            if confidence > min_confidence:
    			# compute the (x, y)-coordinates of the bounding box for
    			# the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

    			# extract the face ROI and grab the ROI dimensions
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

    			# ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue
                # construct a blob for the face ROI, then pass the blob
    			# through our face embedding model to obtain the 128-d
    			# quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

    			# add the name of the person + corresponding face
    			# embedding to their respective lists
                knownNames.append(name)
                knownEmbeddings.append(vec.flatten())
                total += 1
    # dump the facial embeddings + names to disk
    print("[INFO] serializing {} encodings...".format(total))
    data = {"embeddings": knownEmbeddings, "names": knownNames}
    f = open("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/output/embeddings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()
