# USAGE
# python detect_faces.py --image rooster.jpg --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#    help="path to input image")
ap.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

percentage_data = "percentage_data.csv"
processing_data = "processing_dta.csv"

# Setup for PyPlot graphs


for it in range(1, 10):

    #count = 4
    og_image = "test_images/test{}.jpg".format(it)
    print(og_image)

        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
    #image = cv2.imread(args["image"])
    image = cv2.imread(og_image)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    #print("Detections 1: %i", detections)

    csv = open(percentage_data, "a")
    csv2 = open(processing_data, "a")
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction

        #Initial time before detection
        time0 = time.time()

        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            print(confidence)
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
         
                # draw the bounding box of the face along with the associated
                # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(image, text, (startX, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

            new_image_name = "image{}.jpg".format(it)
                #print("{}, {}, {}".format(image_name, i, confidence))
            output = "{}, {}\n".format(it, confidence)
            csv.write(output)

                # show the output image
                #cv2.imshow("Output", image)
            cv2.imwrite('results/{}'.format(new_image_name), image)
            

            #Calculate the time needed to procces each detection
            time1 = time.time()
            diff = time1 - time0
            csv2.write("{}, {}\n".format(it, diff))
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

