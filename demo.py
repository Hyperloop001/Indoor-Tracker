#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import os
from timeit import time
import warnings
import sys
import cv2
import numpy as np
from PIL import Image
from yolo import YOLO

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet


from deep_sort.traceRecording.humanTraceRecorder import HumanTraceRecorder
from deep_sort.traceRecording.faceRecognition import *


warnings.filterwarnings('ignore')

def main(yolo):

   # Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0
    
   # deep_sort 
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename,batch_size=1)
    
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    writeVideo_flag = False
    
    #video_capture = cv2.VideoCapture("rtsp://admin:admin@192.168.30.81:554/3")


    #video_capture = cv2.VideoCapture("test.mp4")


    video_capture = cv2.VideoCapture(0)

    if writeVideo_flag:
    # Define the codec and create VideoWriter object
        w = int(video_capture.get(3))
        h = int(video_capture.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1 
        
    fps = 0.0


    htr = HumanTraceRecorder()
    frameCounter = 0
    while True:
        ret, frame = video_capture.read()  # frame shape 640*480*3


        #frame = cv2.resize(frame,(640,360), interpolation=cv2.INTER_LINEAR)

        if ret != True:
            break;
        t1 = time.time()

        image = Image.fromarray(frame)
        boxs = yolo.detect_image(image)
       # print("box_num",len(boxs))
        features = encoder(frame,boxs)
        
        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
        
        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]
        
        # Call the tracker
        tracker.predict()
        tracker.update(detections)


        for track in tracker.tracks:
            if track.is_confirmed() and track.time_since_update >1 :
                continue 
            bbox = track.to_tlbr()
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            print(track.name_id)

            if (frameCounter % 5) == 0:


                x = int((bbox[0] + bbox[2]) / 2)
                y = int((bbox[1] + bbox[3]) / 2)
                new_time = frameCounter

                if track.name_id != 0:  # this is a tracked person
                    htr.updatePerson(track.name_id, x, y, new_time)
                else:
                    subimage = image.crop((int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))
                    subimagearr = np.asarray(subimage)
                    faceID = getFaceID(subimagearr, predictor_path = "./deep_sort/traceRecording/shape_predictor_5_face_landmarks.dat",
                                       face_rec_model_path = "./deep_sort/traceRecording/dlib_face_recognition_resnet_model_v1.dat")
                    if faceID == 0:
                        print("No face found")
                    else:
                        find, name_id = htr.checkPerson(faceID)
                        if find:
                            track.name_id = htr.updatePerson(name_id, x, y, new_time)
                        else:
                            track.name_id = htr.addNewPerson(faceID, x, y, new_time)


            cv2.putText(frame, str(track.name_id), (int(bbox[0]), int(bbox[1])), 0, 5e-3 * 200, (0, 255, 0), 2)
        frameCounter += 1

        """
            if track.track_id != 0: # this is a tracked person
                dataBase.addPersonTrace(track.track_id, location) # add the new location to the person's trace
            else :  # new detected person, need to verify the identity
            
            
                subimage = image(cv2.Rect(int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))
                result = faceDetect(subimage) # result should be the face data detected


                if result: # make sure there is a face detection
                    if dataBase.checkPerson(result): # check if the person was recorded before
                        name = dataBase.checkName(result)
                    else: # new person, add to dataBase
                        newName = XXXXXXXXX # XXXXXXXXX is the new name
                        dataBase.addPerson(result, newName) 
                        name = newName
                    dataBase.addPersonTrace(name, location) # add the new location to the person's trace

                    track.track_id = name
                else : # no face detected, cannot identify the person
                    # do nothing, leave track unchange and wait for the next chance
        """



        for det in detections:
            bbox = det.to_tlbr()
            cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,0,0), 2)



            
        cv2.imshow('', frame)
        
        if writeVideo_flag:
            # save a frame
            out.write(frame)
            frame_index = frame_index + 1
            list_file.write(str(frame_index)+' ')
            if len(boxs) != 0:
                for i in range(0,len(boxs)):
                    list_file.write(str(boxs[i][0]) + ' '+str(boxs[i][1]) + ' '+str(boxs[i][2]) + ' '+str(boxs[i][3]) + ' ')
            list_file.write('\n')
            
        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        print("fps= %f"%(fps))
        
        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    if writeVideo_flag:
        out.release()
        list_file.close()
    cv2.destroyAllWindows()

    htr.saveToFile()

if __name__ == '__main__':
    main(YOLO())
