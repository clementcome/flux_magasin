# USAGE
# python multi_object_tracking_slow.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt \
#	--model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --video race.mp4
#python test16.3.py -m goturn.caffemodel -p goturn.prototxt -v Crowd-Activity-All.avi
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
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
args = vars(ap.parse_args())

# initialize the video stream and output video writer
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(args["video"])
writer = None

points = np.zeros((4,2))
global n_points
n_points = 0
global go 
go = False
def draw_circle(event,x,y,flags,param):
	global mouseX,mouseY
	global n_points
	global go
	if event == cv2.EVENT_LBUTTONDBLCLK:

		mouseX,mouseY = x,y
		points[n_points][0] = x
		points[n_points][1] = y

		if n_points == 0:
			cv2.circle(frame,(x,y),3,(0,0,0))
		
		elif 3 > n_points > 0:
			old_x, old_y = int(points[n_points - 1][0]), int(points[n_points - 1][1])
			cv2.line(frame, (old_x, old_y), (x,y), (0,0,0), 5)
		
		else:
			old_x, old_y = int(points[0][0]), int(points[0][1])
			cv2.line(frame, (old_x, old_y), (x,y), (0,0,0), 5)

			old_x, old_y = int(points[n_points - 1][0]), int(points[n_points - 1][1])
			cv2.line(frame, (old_x, old_y), (x,y), (0,0,0), 5)

			n_points -= n_points
			go = True

		n_points += 1

def define_real_coord(points, dimentions, frame, A):
	"""
	"""
	#define variables
	N = len(points)

	#determine correct order
	maxx = 10000
	i_x = 0
	for i in range(N):
		
		if np.linalg.norm(points[i]) <= maxx:
			maxx = np.linalg.norm(points[i])
			i_x = i
	
	if np.cross(points[i_x], points[(i_x + 1) % N]) < 0:
		x = int(points[(i_x)][0])
		y = int(points[(i_x)][1])
		cv2.circle(frame,(x,y),10,(0,255,0))
		sense = -1
	else:
		x = int(points[(i_x)][0])
		y = int(points[(i_x)][1])
		cv2.circle(frame,(x,y),10,(0,255,0))
		sense = 1

	p1 = [0,0]
	p2 = [0,dimentions[0] - 1]
	p3 = [dimentions[1] - 1,dimentions[0] - 1]
	p4 = [dimentions[1] - 1, 0]
	target = np.array([p1,p2,p3,p4])

	ordered_points = np.zeros((4,2))
	for i in range(4):

		x = points[(i_x + N + sense * i) % N][0]
		y = points[(i_x + N + sense * i) % N][1]
		ordered_points[i] = (x,y)

		cv2.putText(frame, str(target[i][0]) + ", " + str(target[i][1]), (int(x),int(y)),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
		cv2.putText(frame, str(x) + ", " + str(y), (int(x),int(y) - 15),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	matrix = []
	for p1, p2 in zip(ordered_points, target):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

	C = np.matrix(matrix, dtype=np.float)
	B = np.array(target).reshape(8)

	temp = np.dot(np.linalg.inv(C.T * C) * C.T, B)
	res = np.array(temp).reshape(8)

	def to_real_coordinates(x,y):
		new_x = (res[0] * x + res[1] * y + res[2]) / (res[6] * x + res[7] * y + 1)
		new_y = (res[3] * x + res[4] * y + res[5]) / (res[6] * x + res[7] * y + 1)
		
		new_x = max(new_x, 0)
		new_y = max(new_y, 0)
		new_x = min(new_x, dimentions[1] - 1)
		new_y = min(new_y, dimentions[0] - 1)
		

		return (new_x, new_y)
	

	for i in range(4):

		x = ordered_points[i][0]
		y = ordered_points[i][1]
		x, y = to_real_coordinates(x,y)

	return to_real_coordinates

def within_bounds(polygon, points):


	p = path.Path(polygon)

	return not (False in p.contains_points(points))



(grabbed, frame) = vs.read()
#cv2.imshow('Frame',frame)


dimentions = frame.shape
A = np.zeros(dimentions)
while(1):
	frame = imutils.resize(frame, width=600)
	A = imutils.resize(A, width=600)
	cv2.imshow('Frame',frame)
	cv2.imshow('Rien',A)
	cv2.setMouseCallback('Frame',draw_circle)
	if go:

		to_real_coordinates = define_real_coord(points, frame.shape[0:2], frame, A)
		go = False
	k = cv2.waitKey(20) & 0xFF
	if k == ord('q'):
		break
	elif k == ord('a'):
		print(mouseX, mouseY)


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
labels = []

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
		# grab the frame dimentions and convert the frame to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)

		# pass the blob through the network and obtain the detections
		# and predictions
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		#for i in np.arange(0, detections.shape[2]):
		for i in np.arange(1, 2):
			# extract the confidence (i.e., probability) associated
			# with the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by requiring a minimum
			# confidence

			if confidence > args["confidence"]:
				# extract the index of the class label from the
				# detections list
				idx = int(detections[0, 0, i, 1])
				label = CLASSES[idx]

				# if the class label is not a person, ignore it
				if CLASSES[idx] != "person":
					continue

				# compute the (x, y)-coordinates of the bounding box
				# for the object
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				if not within_bounds(points, [((startX + endX)/2, (startY + endY)/2)]):
					continue
				
				mx, my = ((startX + endX)/2, (startY + endY)/2)
				rmx, rmy = to_real_coordinates(mx, my)
				cv2.circle(A, ((int(rmx), int(rmy))), 3, (255,255,0), thickness = 2)

				# construct a dlib rectangle object from the bounding
				# box coordinates and start the correlation tracker
				t = cv2.TrackerGOTURN_create() 
				rect = (startX, startY, endX, endY)
				
				ok = t.init(frame,rect)

				# update our set of trackers and corresponding class
				# labels
				labels.append(label)
				trackers.append(t)

				# grab the corresponding class label for the detection
				# and draw the bounding box
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 255, 0), 2)

				print("Here")

	# otherwise, we've already performed detection so let's track
	# multiple objects
	else:

		# loop over each of the trackers
		for (t, l) in zip(trackers, labels):
			
			print(l)
			# update the tracker and grab the position of the tracked
			# object
			#t.update(frame)
			ok, box = t.update(frame)


			# unpack the position object
			startX = int(box[0])
			startY = int(box[1])
			endX = int(box[2])
			endY = int(box[3])

			mx, my = ((startX + endX)/2, (startY + endY)/2)
			
			if not within_bounds(points, [(mx, my)]):
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(255, 0, 0), 2)
				continue


			rmx, rmy = to_real_coordinates(mx, my)

			cv2.circle(A, ((int(rmx), int(rmy))), 3, (255,255,0), thickness = 2)

			# draw the bounding box from the correlation object tracker
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 255, 0), 2)
			cv2.putText(frame, l, (startX, startY - 15),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	# check to see if we should write the frame to disk
	if writer is not None:
		writer.write(frame)

	# show the output frame
	#cv2.imshow("Frame", frame)	
	cv2.imshow("Other", A)
	cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()



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