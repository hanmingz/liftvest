# OpenCV program to perform Edge detection in real time
# import libraries of python OpenCV 
# where its functionality resides
import cv2 
import time
# np is an alias pointing to numpy library
import numpy as np
 
 
# capture frames from a camera
cap = cv2.VideoCapture(0)
 
count = 0
# loop runs if capturing has been initialized
while(1):
    # reads frames from a camera
    ret, frame = cap.read()
 
    # converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
    # define range of red color in HSV
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
     
    # create a red HSV colour boundary and 
    # threshold HSV image
    mask = cv2.inRange(hsv, lower_red, upper_red)
 
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
 
    # Display an original image
    # cv2.imshow('Original',frame)
 
    # finds edges in the input image image and
    # marks them in the output map edges
    edges = cv2.Canny(frame,100,200)
    # cv2.imshow('Edges',edges)
    start_time = time.time()
    circles = cv2.HoughCircles(edges,cv2.cv.CV_HOUGH_GRADIENT,1,100,
        param1=50,param2=25,minRadius=20,maxRadius=80)
    disp = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            print("there is circle!!!", count)
            count=count+1
            # draw the outer circle
            cv2.circle(disp,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(disp,(i[0],i[1]),2,(0,0,255),3)
        if len(circles) == 3:
    	    print(circles)

   	if len(circles[0]) == 3:
		pC = circles[0][0] #always calculating the angle at vertex C
		pA = circles[0][1]
		pB = circles[0][2]
		cv2.line(disp, (pA[0], pA[1]), (pB[0], pB[1]), (0,0,255), 5)
		cv2.line(disp, (pC[0], pC[1]), (pA[0], pA[1]), (0,0,255), 5)
		cv2.line(disp, (pC[0], pC[1]), (pB[0], pB[1]), (0,0,255), 5)

		disAB = np.sqrt(np.power(pB[0]-pA[0],2) +np.power(pB[1]-pA[1],2))
		disBC = np.sqrt(np.power(pB[0]-pC[0],2) +np.power(pB[1]-pC[1],2))
		disAC = np.sqrt(np.power(pC[0]-pA[0],2) +np.power(pC[1]-pA[1],2))
		cosTheta = (np.power(disBC, 2) + np.power(disAC, 2) - np.power(disAB, 2)) / (2*disBC*disAC)
		theta = np.arccos(cosTheta) * 180 / np.pi
		print theta #should be close to 180
		if theta < 190 and theta > 170:
			print("back is straight")
		else:
			print("back is bent")

    cv2.imshow('Edges',disp)

    # print ("My program took", time.time() - start_time, "to run")
 
    # Wait for Esc key to stop
    k = cv2.waitKey(50) & 0xFF
    if k == 27:
        break
 
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows() 