import cv2
import pickle


# img = cv2.imread('carParkImg.png')

width, height = 107, 48

try:
    with open('CarParkPos','rb') as f:
        postlist = pickle.load(f)
except:
    postlist = []

def mouseClick(events, x,y,flags, params):
    if events == cv2.EVENT_FLAG_LBUTTON:
        postlist.append((x,y))
    if events == cv2.EVENT_FLAG_RBUTTON:
        for i, pos in enumerate(postlist):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                postlist.pop(i)

    with open('CarParkPos','wb') as f:
        pickle.dump(postlist,f)


while True:
    img = cv2.imread('carParkImg.png')
    # cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)

    for pos in postlist:
        cv2.rectangle(img,pos,(pos[0]+width, pos[1]+height),(255,0,255),2)

    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)
