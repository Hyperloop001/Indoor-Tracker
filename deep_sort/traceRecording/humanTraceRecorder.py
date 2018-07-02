#!/usr/bin/python

from .human import Human
import sys
import os
import dlib
import glob

class HumanTraceRecorder:
    """
    class: HumanTraceRecorder
    Fields:
        listOfHuman (a list of Human)
        humanIDCounter

    """
    def __init__(self):
        self.listOfHuman = []
        self.humanIDCounter = 1

    """
    
    def addNewPerson(self, name, faceID):
        self.listOfHuman.append(Human(name, faceID))

    def matchPerson(self, faceID):
        for person in self.listOfHuman:
            if person.isFaceMatched(faceID):
                return person
        return 0
    

    def updateOrAddPerson(self, faceID, x, y, new_time):
        rv = self.humanIDCounter
        for person in self.listOfHuman:
            if person.isFaceMatched(faceID):
                person.addToTrace(x, y, new_time)
                print("Update human trace at time %d:" % new_time)
                print("  NameID: %d" % person.name)
                print("  Coordinate: (%d, %d)" % (x, y))
                return rv

        self.listOfHuman.append(Human(self.humanIDCounter, faceID))
        self.listOfHuman[-1].addToTrace(x, y, new_time)
        print("Create human trace at time %d:" % new_time)
        print("  NameID: %d" % self.humanIDCounter)
        print("  Coordinate: (%d, %d)" % (x, y))
        self.humanIDCounter += 1
        return rv
        
    """

    def updatePerson(self, nameID, x, y, new_time):
        self.listOfHuman[nameID - 1].addToTrace(x, y, new_time)
        print("Update human trace at time %d:" % new_time)
        print("  NameID: %d" % self.listOfHuman[nameID - 1].name)
        print("  Coordinate: (%d, %d)" % (x, y))
        return nameID


    def addNewPerson(self, faceID, x, y, new_time):
        rv = self.humanIDCounter
        self.listOfHuman.append(Human(rv, faceID))
        self.listOfHuman[-1].addToTrace(x, y, new_time)
        print("Create human trace at time %d:" % new_time)
        print("  NameID: %d" % rv)
        print("  Coordinate: (%d, %d)" % (x, y))
        self.humanIDCounter += 1
        return rv


    def checkPerson(self,faceID):
        index = 1
        find = False
        for person in self.listOfHuman:
            if person.isFaceMatched(faceID):
                find = True
                rv = index
                break
            else:
                index += 1
        if find:
            return True, rv
        else:
            return False, None



    # def loadFromFile(self, path):


    def saveToFile(self):
        logFile = open("log.txt", 'w+')
        faceFile = open("face.txt", 'w+')
        for person in self.listOfHuman:


            faceFile.write("%d [ " % person.name)
            for i in range(len(person.faceID)):
                faceFile.write("%f " % person.faceID[i])


            logFile.write("%d [ " % person.name)
            for j in range(len(person.tracePosition)):
                logFile.write("(%d, %d, %s) " % (person.tracePosition[j].x, person.tracePosition[j].y, str(person.traceTime[j])))
            logFile.write("]\n")
            faceFile.write("]\n")

        logFile.close()
        faceFile.close()
        print("log saved")



