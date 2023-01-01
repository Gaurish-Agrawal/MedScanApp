import cmake
import dlib
import face_recognition
import cv2
import numpy as np
import os
import re
import pickle
from app.db import User

def returndata(url):

    directory = 'faces'
    known_face_encodings= []

    images = []
    for face in os.listdir(directory):
        images.append(face)
    images.sort()

    if images[0]==".DS_Store":
        images = images[1:]

    

    for face in images:
        im = cv2.imread(directory + "/"+ face)
        h, w, _ = im.shape
        currentFace = face_recognition.load_image_file(directory + "/"+ face)
        current_face_encoding = face_recognition.face_encodings(currentFace)
        if len(current_face_encoding)>0:
            known_face_encodings.append(current_face_encoding[0])


        """
        im = cv2.imread(directory + "/"+ face)
        h, w, c = im.shape
        currentFace = face_recognition.load_image_file(directory + "/"+ face)
        known_face_locations=[(0, w, h, 0)]
        current_face_encoding = face_recognition.face_encodings(currentFace,known_face_locations)[0]
        known_face_encodings.append(current_face_encoding)
        """
        #currentFace = face_recognition.load_image_file(directory + "/"+ face)
        #face_locations = face_recognition.face_locations(currentFace)
        #current_face_encoding = face_recognition.face_encodings(currentFace,face_locations)[0]
        #known_face_encodings.append(current_face_encoding)

        """
    for face in images:
        im = cv2.imread(directory + "/"+ face)
        h, w, c = im.shape
        currentFace = face_recognition.load_image_file(directory + "/"+ face)
        known_face_locations=[(0, w, h, 0)]
        current_face_encoding = face_recognition.face_encodings(currentFace,known_face_locations)[0]
        known_face_encodings.append(current_face_encoding)

        
        face_locations = face_recognition.face_locations(currentFace)
        try:
            current_face_encoding = face_recognition.face_encodings(currentFace,face_locations)
            print(current_face_encoding,"\n\n\n")
            known_face_encodings.append(current_face_encoding[0])
        except IndexError as e:
            print(e)
        """



    #known_face_names = ['Aniket Gupta', 'Gaurish Agrawal']
    #known_face_names.sort()

    #Aaron Eckhart', 'Aaron Patterson', 'Aaron Peirsol', 'Aaron Sorkin', 'Aaron Tippin', 'Abba Eban', 'Abbas Kiarostami',  'Abdul Rahman', 'Abdulaziz Kamilov', 'Abdullah Nasseef',
    #'Abdullatif Sener', 'Abel Pacheco', 'Abner Martinez','Abraham Foxman', 'Aniket Gupta', 'Bill Paxton', 'Joe Biden',
    #'Gaurish Agrawal', "Kabir Rakshe", 'Donald Trump', 'Barack Obama','Ben Chandler','Debbie Allen','Elizabeth Regan','Emma Watson', 'Diana Munz', 'Choi Sung-Hong', 'Chris Bell']

    
                    


    known_face_names = []
    with open('file.pkl', 'rb') as pickle_load:
        known_face_names = pickle.load(pickle_load)

    known_face_names = list(set(known_face_names))
    known_face_names.sort()


    #print(known_face_names)
    #print(images)



    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True


    frame = cv2.imread(url)

    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            print(matches)

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                if name!="Unknown":
                    print(name,"\n\n\n\n\n\n\n\n")

                    users = User.query.all()
                    for user in users:
                        print(user.name)

                    query = User.query.filter_by(name=name).first()
                    data = [query.gender,query.birthday,query.height,query.age,[query.condition],query.econtact,query.name]
                    return data
                    
                else:
                    return None


            face_names.append(name)