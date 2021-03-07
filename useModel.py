import cv2
import imutils
import numpy as np
import tensorflow
from idLetter import idLetter
import os

# global variables
bg = None

# Choose active camers
camera = 0

fileLocation = os.path.dirname(os.path.realpath(__file__))

model = tensorflow.keras.models.load_model(
    fileLocation + '\\final_model.h5')
TM_DATA = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
f = open(fileLocation + '\\final_labels.txt', 'r')
labels = f.read().split('\n')[:-1]
# Fix this

stats = idLetter(labels)
letter = ''
wordEnd = False

# --------------------------------------------------
# To find the running average over the background
# --------------------------------------------------


def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)

    # ---------------------------------------------
    # To segment the region of hand in the image
    # ---------------------------------------------


def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    (cnts, _) = cv2.findContours(thresholded.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


# -----------------
# MAIN FUNCTION
# -----------------
if __name__ == "__main__":
    # initialize weight for running average
    aWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(camera)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 100, 250, 300, 450

    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = cv2.resize(frame, (700, 700))

        # flip the frame so that it is not the mirror view
        viewFrame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                wordEnd = False
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # draw the segmented region and display the frame
                cv2.drawContours(
                    clone, [segmented + (right, top)], -1, (0, 0, 255))
                img2 = np.zeros_like(roi)
                img2[:, :, 0] = thresholded
                img2[:, :, 1] = thresholded
                img2[:, :, 2] = thresholded
                thresholded = img2
                cv2.imshow("Thesholded", cv2.flip(thresholded, 1))

                thresholded = cv2.resize(roi, (224, 224))
                image_array = np.asarray(thresholded)
                normalized = (image_array.astype(np.float32)/127.0)-1
                TM_DATA[0] = normalized
                PredictionVar = model.predict(TM_DATA)
                # print(PredictionVar)
                # print(max(PredictionVar[0]))
                # print(labels[PredictionVar[0].tolist().index(
                #     max(PredictionVar[0]))])
                c = stats.addData(labels[PredictionVar[0].tolist().index(
                    max(PredictionVar[0]))], max(PredictionVar[0]))
                if c is not None:
                    letter = c
                    print(letter[2:])

                # idLetter(max(PredictionVar[0]), labels[PredictionVar[0].tolist().index(
                #     max(PredictionVar[0]))])
                #labels[np.where(PredictionVar[0] == max(PredictionVar[0]))]
            else:
                wordEnd = True

        # draw the segmented hand
        cv2.rectangle(viewFrame, (left, top), (right, bottom), (0, 255, 0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", viewFrame)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break


# free up memory
camera.release()
cv2.destroyAllWindows()
