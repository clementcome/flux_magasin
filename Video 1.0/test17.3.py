# USAGE
# python multi_object_tracking_slow.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt \
#	--model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --video race.mp4
#python test17.3.py -p mobilenet_ssd/MobileNetSSD_deploy.prototxt -m mobilenet_ssd/MobileNetSSD_deploy.caffemodel -v Crowd-Activity-All.avi
# import the necessary packages
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import dlib
import cv2
from scipy import stats
from sklearn import linear_model
from matplotlib import path
import matplotlib.pyplot as plt
import pickle

def load_path(file = "boxes.txt"):
	with open(file, "rb") as f:
		return pickle.load(f)

def save_path(paths, file = "paths.txt"):

	with open(file, "wb") as f:
		pickle.dump(paths, f)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
ap.add_argument("-o", "--output", type=str,
	help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.35,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
args = vars(ap.parse_args())

# initialize the video stream and output video writer
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(args["video"])
writer = None

#Initialize variables
#points is the list of points that defien the bounding box
points = np.zeros((4,2))
global n_points
n_points = 0
global go 
go = False

def draw_circle(event,x,y,flags,param):
	'''
	<- event (opencv event), x (int), y (int), flags, param
	-> None
	Creates a circle on the clicked location. It is designed to be set as 
	the default response click response with cv2.setMouseCallback()
	'''

	#utilize global variables (ugly method, maybe change)
	global mouseX,mouseY
	global n_points
	global go

	#only cares about left click
	if event == cv2.EVENT_LBUTTONDBLCLK:

		#add the point to the list of points
		mouseX,mouseY = x,y
		points[n_points][0] = x
		points[n_points][1] = y

		#For the first point just draw a circe
		if n_points == 0:
			cv2.circle(frame,(x,y),3,(0,0,0))
		
		#For the second and third draw lines
		elif 3 > n_points > 0:
			old_x, old_y = int(points[n_points - 1][0]), int(points[n_points - 1][1])
			cv2.line(frame, (old_x, old_y), (x,y), (0,0,0), 5)
		
		#For the fourth draw the two lines
		else:
			old_x, old_y = int(points[0][0]), int(points[0][1])
			cv2.line(frame, (old_x, old_y), (x,y), (0,0,0), 5)

			old_x, old_y = int(points[n_points - 1][0]), int(points[n_points - 1][1])
			cv2.line(frame, (old_x, old_y), (x,y), (0,0,0), 5)

			#written like this to avoid confucion with local variables
			n_points -= n_points
			go = True

		n_points += 1

def define_real_coord(points, dimentions, frame, A):
	"""
	-> points (numpy matrix), dimension (couple), frame (opencv image), A (opencv image)
	<- to_real_coordinates (python function)
	Defines the function to translate video coordiantes to "real" coordiantes
	"""

	#define variables
	N = len(points)

	#determine clockwise order of points
	#initialize search for the minimum norm
	maxx = 10000
	i_x = 0
	#find point of minimum norm
	for i in range(N):
		
		if np.linalg.norm(points[i]) <= maxx:
			maxx = np.linalg.norm(points[i])
			i_x = i
	
	#determine clockwise sense
	if np.cross(points[i_x], points[(i_x + 1) % N]) < 0:
		sense = -1
	else:
		sense = 1

	#p1 to p4 are the "real" points corresponding to the ends of the bounding box
	p1 = [0,0]
	p2 = [0,dimentions[0] - 1]
	p3 = [dimentions[1] - 1,dimentions[0] - 1]
	p4 = [dimentions[1] - 1, 0]
	target = np.array([p1,p2,p3,p4])

	#put the points in an array in the rigth order
	ordered_points = np.zeros((4,2))
	for i in range(4):

		#iterate over the points in a clockwise sense
		x = points[(i_x + N + sense * i) % N][0]
		y = points[(i_x + N + sense * i) % N][1]
		ordered_points[i] = (x,y)

		#write their real and video coordinates on the image
		cv2.putText(frame, str(target[i][0]) + ", " + str(target[i][1]), (int(x),int(y)),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
		cv2.putText(frame, str(x) + ", " + str(y), (int(x),int(y) - 15),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	#solve the perspective problem (copyed method, must review)
	matrix = []
	for p1, p2 in zip(ordered_points, target):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

	C = np.matrix(matrix, dtype=np.float)
	B = np.array(target).reshape(8)

	temp = np.dot(np.linalg.inv(C.T * C) * C.T, B)
	res = np.array(temp).reshape(8)

	#define the coordinate transformation function
	def to_real_coordinates(x,y):
		'''
		-> x (float), y (float)
		<- new_x (float), new_y (float)
		'''

		#apply linear transformation
		new_x = (res[0] * x + res[1] * y + res[2]) / (res[6] * x + res[7] * y + 1)
		new_y = (res[3] * x + res[4] * y + res[5]) / (res[6] * x + res[7] * y + 1)
		
		#crop if sligthly outside of bounds
		new_x = max(new_x, 0)
		new_y = max(new_y, 0)
		new_x = min(new_x, dimentions[1] - 1)
		new_y = min(new_y, dimentions[0] - 1)
		

		return (new_x, new_y)
	
	return to_real_coordinates

def within_bounds(polygon, points):
	'''
	-> polygon (list of points), points (list of points)
	<- bool
	Determines if any of the elements of points is outside the area defined by polygon
	'''

	p = path.Path(polygon)

	return not (False in p.contains_points(points))


#read frame from video
(grabbed, frame) = vs.read()

#define the dimentions of the window (done randomly, should do properly)
dimentions = (400, 200)

#initialize the "real" coordinate matrix
A = np.zeros(dimentions)

#First loop with fixed image to mark bounding box

#Resize the images
frame = imutils.resize(frame, width=600)
A = imutils.resize(A, width=600)

while(1):
	#Show the image so the box can be set
	cv2.imshow('Frame',frame)
	#Define the callback to drax the square
	cv2.setMouseCallback('Frame',draw_circle)

	#Define the coordinate transformation
	if go:

		to_real_coordinates = define_real_coord(points, frame.shape[0:2], frame, A)
		go = False

	#wait for key, with q pass to next step
	k = cv2.waitKey(20) & 0xFF
	if k == ord('q'):
		break


# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream and output video writer
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(args["video"])
writer = None

# initialize the list of object trackers and corresponding class
# labels
trackers = []
paths = []

# start the frames per second throughput estimator
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the next frame from the video file
	(grabbed, frame) = vs.read()

	# check to see if we have reached the end of the video file
	if frame is None:
		break

	# resize the frame for faster processing and then convert the
	# frame from BGR to RGB ordering (dlib needs RGB ordering)
	frame = imutils.resize(frame, width=600)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# if we are supposed to be writing a video to disk, initialize
	# the writer
	if args["output"] is not None and writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)

	# if there are no object trackers we first need to detect objects
	# and then create a tracker for each object
	if len(trackers) == 0:
		# load the predefined boxes
		boxes = load_path()

		# loop over the boxes
		for box in boxes:


			# extract the index of the class label from the
			# detections list


			(startX, startY, dX, dY) = box

			mx, my = (startX + (dX)/2, (startY + dY))
			rmx, rmy = to_real_coordinates(mx, my)
			cv2.circle(A, ((int(rmx), int(rmy))), 3, (255,255,0), thickness = 2)

			# construct a dlib rectangle object from the bounding
			# box coordinates and start the correlation tracker
			t = dlib.correlation_tracker()
			rect = dlib.rectangle(startX, startY, startX + dX, startY + dY)
			t.start_track(rgb, rect)

			# update our set of trackers and corresponding class
			# labels

			trackers.append(t)

			# grab the corresponding class label for the detection
			# and draw the bounding box
			cv2.rectangle(frame, (startX, startY), (dX + startX, startY + dY),
				(0, 255, 0), 2)

		paths = [0] * len(trackers)
		for i in range(len(trackers)):
			paths[i] = []
			
	# otherwise, we've already performed detection so let's track
	# multiple objects
	else:

		# loop over each of the trackers
		for k in range(len(trackers)):
			t = trackers[k]
				
			# update the tracker and grab the position of the tracked
			# object
			t.update(rgb)
			pos = t.get_position()


			# unpack the position object
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())

			mx, my = ((startX + endX)/2, (endY))
			
			if not within_bounds(points, [(mx, my)]):
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(255, 0, 0), 2)

				paths[k].append(np.array([-12, -12]))
				continue


			rmx, rmy = to_real_coordinates(mx, my)
			print((rmx, rmy))
			print(k)
			paths[k].append(np.array([rmx, rmy]))
			cv2.circle(A, ((int(rmx), int(rmy))), 3, (255,255,0), thickness = 2)

			# draw the bounding box from the correlation object tracker
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 255, 0), 2)

	# check to see if we should write the frame to disk
	if writer is not None:
		writer.write(frame)

	# show the output frame
	cv2.imshow("Frame", frame)	
	cv2.imshow("Other", A)
	
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()
	#trackers.clear()

real_path = []
for i in range(len(paths)):
	if len(paths[i]) > 0:
		real_path.append(paths[i])

save_path(real_path)
# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# check to see if we need to release the video writer pointer
if writer is not None:
	writer.release()

# do a bit of cleanup
cv2.destroyAllWindows()
vs.release()