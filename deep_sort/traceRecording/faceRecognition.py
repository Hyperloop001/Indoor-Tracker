import dlib
from PIL import Image
import numpy as np


# img is an array type
def getFaceID(img, predictor_path = "shape_predictor_5_face_landmarks.dat", face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"):
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    if len(dets) == 0:
        return 0

    # Now process each face we found.
    box = dets[0]
    shape = sp(img, box)
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    return face_descriptor




if __name__ == '__main__':
    img = np.array(Image.open("./faceImages/BillFace.jpg"))
    vec = getFaceID(img)
    print(vec)


