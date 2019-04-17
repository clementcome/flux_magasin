# USAGE
# python multi_object_tracking.py --video Crowd-Activity-All.avi --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import numpy as np
import pickle

def save_path(paths, file = "paths.txt"):

	with open(file, "wb") as f:
		pickle.dump(paths, f)



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())



# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()

# initialize create Background Subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((5,5),np.float32)/25
change = False
A = np.zeros((337, 600, 3))
first = True
save = []
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])


# resize the frame (so we can process it faster)

frame = vs.read()
# grab the current frame, then handle if we are using a
# VideoStream or VideoCapture object
frame = frame[1] if args.get("video", False) else frame
frame = imutils.resize(frame, width=600)

# loop over frames from the video stream
while True:

	# check to see if we have reached the end of the stream
	if frame is None:
		break



	# show the output frame
	cv2.imshow("Frame", frame)


	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		
		break
	
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		save.append(box)
		print(box)
		(startX, startY, endX, endY) = box
		cv2.rectangle(frame, (startX, startY), (endX + startX, endY + startY),
					(0, 255, 0), 2)

# if we are using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()

# otherwise, release the file pointer
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
save_path(save, "boxes.txt")