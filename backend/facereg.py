from PIL import Image
import face_recognition
import sys
import math
import numpy as np
from operator import itemgetter
import pandas as pd

def face_to_name(image_path):
    unknown_image = face_recognition.load_image_file(image_path)

    ans = {}
    known_people = []
    data = pd.read_csv('data/students.csv').values
    for d in data:
        my_face_loaded = face_recognition.load_image_file('data/' + d[1])
        my_face_encoding = face_recognition.face_encodings(my_face_loaded)[0]
        known_people.append((d[0], my_face_encoding))

    face_locations = face_recognition.face_locations(unknown_image)

    for face in face_locations:
        top, right, bottom, left = face

        face_image = unknown_image[int(0.8*top):int(1.2*bottom), int(0.8*left):int(1.2*right)]

        x = (right+left)/2
        y = (top+bottom)/2

        if len(face_recognition.face_encodings(np.array(face_image), model='large')) == 0:
            Image.fromarray(face_image).show()

        
        unknown_face_encoding = face_recognition.face_encodings(np.array(face_image), model='large')[0]

        for (name, face_pos) in known_people:
            print(face_recognition.compare_faces([face_pos], unknown_face_encoding, tolerance=0.5)[0])
            if face_recognition.compare_faces([face_pos], unknown_face_encoding, tolerance=0.5)[0]:
                ans[name] = (x, y)
                break
            else:
                print("Unknown face")

    print(ans)
    return ans

    
def nearest_hand(facex, facey, hands):
    min_dist = sys.float_info.max
    nearest_answer = None
    for hand in hands:
        euclidean = ((facex-hand['x'])**2+(facey-hand['y'])**2)**0.5
        if euclidean < min_dist:
            min_dist = euclidean
            nearest_answer = hand['fingers_up']
    return nearest_answer