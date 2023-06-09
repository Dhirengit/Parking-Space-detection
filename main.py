import cv2
import pickle
import cvzone
import numpy as np


#    Video Feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
        postlist = pickle.load(f)
width, height = 107, 48

def check_parking_space(imgpro):
    space_cnt = 0
    for pos in postlist:
        x,y = pos

        imageCrop = imgpro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imageCrop)
        count = cv2.countNonZero(imageCrop)
        
        if count < 900:
            color = (0,255,0) 
            thick = 5
            space_cnt += 1 
        else:
            color = (0,0,255)
            thick = 2
        cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height),color,thick)
        cvzone.putTextRect(img, str(count), (x,y+height-3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f"Free{space_cnt}/{len(postlist)}", (100,50), scale=3,thickness=5, offset=20, colorR=(0,200,0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,
                                        255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)

    kernal = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernal, iterations=1)

    check_parking_space(imgDilate)
    # for pos in postlist:
    #     cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height),(255,0,255),2)
         

    cv2.imshow("Image",img)
    # cv2.imshow("ImageBlur",imgBlur)
    # cv2.imshow("imgThreshold",imgThreshold)
    # cv2.imshow("imgMedian",imgMedian)
    cv2.waitKey(10)