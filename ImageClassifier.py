import cv2
import numpy as np
import math
import os


path = 'data/cards'
sift = cv2.SIFT_create()
cards = []
classNames = []
list = os.listdir(path)

for cl in list:
    imCur = cv2.imread(f'{path}/{cl}',0)
    cards.append(imCur)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

def findDescriptor(cards):
    descriptList = []
    for card in cards:
        points, descriptor = sift.detectAndCompute(card, None)
        descriptList.append(descriptor)
    return descriptList


def findID(img, descriptList, thresh = 15):
    points2, descriptor2 = sift.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for descriptor in descriptList:
            matches = bf.knnMatch(descriptor, descriptor2, k=2)
            matches_good = []
            for m, n in matches:
                if m.distance < .5 * n.distance:
                    matches_good.append([m])
            matchList.append(len(matches_good))
    except:
        pass
    #print(matchList)
    if len(matchList) != 0:
        if max(matchList) > thresh:
            finalVal = matchList.index(max(matchList))
    return finalVal

descriptList = findDescriptor(cards)
print(len(descriptList))

cap = cv2.VideoCapture(0)

while True:
    success, img =cap.read();
    #cv2.normalize(img, img, 50, 255, cv2.NORM_MINMAX)
    id = findID(img, descriptList)
    if id != -1:
        cv2.putText(img, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 255, 0), thickness = 2)

    cv2.imshow('Capture', img)
    cv2.waitKey(1)









