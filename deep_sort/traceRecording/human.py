#!/usr/bin/python

import sys
import os
import dlib
import glob
import numpy as np
from faceRecognition import *

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Human:
    """
    class: Human
    Fields:
        name (serial number)
        faceID (128D data)
        tracePosition (tracking location result)
        traceTime (tracking time result)
    """
    def __init__(self, name, faceID):
        self.name = name
        self.faceID = faceID
        self.tracePosition = []
        self.traceTime = []


    ### Check if faceID match the human
    def isFaceMatched(self, faceID):
        arr = [np.power((self.faceID[i] - faceID[i]), 2) for i in range(128)]
        euclideanDistance = np.sqrt(np.sum(arr))
        print("EU distance is: %f" % euclideanDistance)
        if(euclideanDistance <= 0.5):
            return True
        else:
            return False

    ### Add to trace
    def addToTrace(self, x, y, new_time):
        self.tracePosition.append(Coordinate(x,y))
        self.traceTime.append(new_time)

#if __name__ == '__main__':