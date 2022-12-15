import cv2
import numpy as np
import math
import os
import time
import threading


class ImageClassifier:

    def __init__(self, onFeatureFound):
        self.sift = cv2.SIFT_create()
        self.classNames, self.cards = self.readData()
        self.descriptList = self.findDescriptor()
        self.featureFound = onFeatureFound  # callback function to call when card detected (requires 1 arg for pokemon label)
        self.detecting = True  # if it is attempting to detect cards

    def readData(self):
        path = os.path.join(os.path.dirname(__file__), "data", "cards")
        cards = []
        classNames = []
        list = os.listdir(path)

        for cl in list:
            imCur = cv2.imread(f'{path}/{cl}', 0)
            cards.append(imCur)
            classNames.append(os.path.splitext(cl)[0])

        return classNames, cards

    def findDescriptor(self):
        descriptList = []
        for card in self.cards:
            points, descriptor = self.sift.detectAndCompute(card, None)
            descriptList.append(descriptor)
        return descriptList

    def findID(self, img, thresh=20):
        points2, descriptor2 = self.sift.detectAndCompute(img, None)
        bf = cv2.BFMatcher()
        matchList = []
        finalVal = -1
        try:
            for descriptor in self.descriptList:
                matches = bf.knnMatch(descriptor, descriptor2, k=2)
                matches_good = []
                for m, n in matches:
                    if m.distance < .5 * n.distance:
                        matches_good.append([m])
                matchList.append(len(matches_good))
        except:
            pass

        if len(matchList) != 0:
            if max(matchList) > thresh:
                finalVal = matchList.index(max(matchList))
        return finalVal

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read();
            id = self.findID(img)
            if id != -1:
                color = (0, 255, 0) if self.detecting else (0, 0, 255)  # red if not detecting, green if it is
                cv2.putText(img, self.classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, color, thickness=2)

                if self.detecting:
                    self.featureFound(self.classNames[id])
                    # only need to detect and perform callback once, then wait for outside source to reset the flag
                    # self.detecting = False    # removed for now, cant think of a good way to re-enable later

            cv2.imshow('Capture', img)
            # exit program when pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    def whenFound(x):
        print(x, "detected in the image")
